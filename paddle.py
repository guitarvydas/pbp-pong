#!/usr/bin/env python3
"""
paddle-controller.py - Interactive paddle controller

Captures up/down arrow keypresses and sends paddle position updates
to daemon.js via TCP port 8081. The daemon forwards them to the
browser GUI over WebSocket.

Usage:
    python3 paddle-controller.py [--id left|right] [--step 10] [--x 50]

Keys:
    Up Arrow    Move paddle up
    Down Arrow  Move paddle down
    q / Ctrl+C  Quit
"""

import sys
import socket
import json
import argparse
import tty
import termios

# ANSI escape sequences for arrow keys
UP_ARROW = b'\x1b[A'
DOWN_ARROW = b'\x1b[B'

DAEMON_HOST = 'localhost'
DAEMON_PORT = 8081

CANVAS_HEIGHT = 600
PADDLE_HEIGHT = 100


def send_command(sock, cmd):
    """Send a JSON command to the daemon over TCP."""
    msg = json.dumps(cmd) + '\n'
    sock.sendall(msg.encode())
    # Read response
    response = sock.recv(1024).decode().strip()
    return response


def main():
    parser = argparse.ArgumentParser(description='Arrow-key paddle controller')
    parser.add_argument('--id', default='left', choices=['left', 'right'],
                        help='Paddle ID (default: left)')
    parser.add_argument('--step', type=int, default=10,
                        help='Pixels per keypress (default: 10)')
    parser.add_argument('--x', type=int, default=None,
                        help='Paddle X position (default: 50 for left, 730 for right)')
    args = parser.parse_args()

    paddle_id = args.id
    step = args.step
    paddle_x = args.x if args.x is not None else (50 if paddle_id == 'left' else 730)

    # Start paddle in the vertical center
    paddle_y = (CANVAS_HEIGHT - PADDLE_HEIGHT) // 2

    # Connect to daemon
    try:
        sock = socket.create_connection((DAEMON_HOST, DAEMON_PORT))
    except ConnectionRefusedError:
        print('Error: Cannot connect to daemon on port %d.' % DAEMON_PORT,
              file=sys.stderr)
        print('Make sure daemon.js is running.', file=sys.stderr)
        sys.exit(1)

    # Send initial paddle position
    cmd = {'type': 'paddle', 'id': paddle_id, 'x': paddle_x, 'y': paddle_y}
    resp = send_command(sock, cmd)

    print('Paddle controller started (%s paddle at x=%d)' % (paddle_id, paddle_x))
    print('  Up/Down arrows to move, q to quit')
    print('  Step size: %d px' % step)
    print('  Current y: %d' % paddle_y)
    print()

    # Save terminal settings and switch to raw mode
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)

        buf = b''
        while True:
            ch = sys.stdin.buffer.read(1)
            if not ch:
                break

            # q or Ctrl-C to quit
            if ch == b'q' or ch == b'\x03':
                break

            # Collect escape sequences
            if ch == b'\x1b':
                buf = ch
                continue
            elif buf == b'\x1b' and ch == b'[':
                buf += ch
                continue
            elif buf == b'\x1b[':
                buf += ch
                seq = buf
                buf = b''

                moved = False
                if seq == UP_ARROW:
                    new_y = paddle_y - step
                    if new_y < 0:
                        new_y = 0
                    if new_y != paddle_y:
                        paddle_y = new_y
                        moved = True
                elif seq == DOWN_ARROW:
                    new_y = paddle_y + step
                    if new_y > CANVAS_HEIGHT - PADDLE_HEIGHT:
                        new_y = CANVAS_HEIGHT - PADDLE_HEIGHT
                    if new_y != paddle_y:
                        paddle_y = new_y
                        moved = True

                if moved:
                    cmd = {'type': 'paddle', 'id': paddle_id,
                           'x': paddle_x, 'y': paddle_y}
                    try:
                        resp = send_command(sock, cmd)
                    except (BrokenPipeError, ConnectionResetError):
                        # Restore terminal before printing error
                        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                        print('\nDaemon disconnected.')
                        sys.exit(1)

                    # Print status (write raw since terminal is in raw mode)
                    status = '\r\x1b[K  y = %d  %s' % (paddle_y, resp)
                    sys.stdout.buffer.write(status.encode())
                    sys.stdout.buffer.flush()
                continue

            # Discard any other input
            buf = b''

    finally:
        # Restore terminal settings
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        sock.close()
        print('\nBye.')


if __name__ == '__main__':
    main()
