# Refactored Dec 31, 2025, 922.00 AM
I asked Claude to refactor all of the code, making the GUI just a slave and the server - on the command line - running all motion logic. [The actual prompt I used is in `prompt.md` in the repo.]

The performance is "not bad" and quite usable, but not as snappy as the previous version. This means that sending ball position messages seems to work well enough, but, the paddle keystroke->server->GUI round trip could be optimized in some way.

aside: This is actually quite encouraging! I'm chewing up a lot of cpu cycles by sending each keystroke through websockets, yet, it works. It could be faster, but it's not terribly slow. I was worried about latencies on the order of seconds, but I'm only seeing latencies in the millisecond range. (20msec is the keystroke latency I remember from the 8-bit days. Humans feel that 20msec is "sluggish" while anything faster than 20msec is "good enough").

The first thought that comes to mind is to create two separate clients - a Left Client and a Right Client. Each client handles its own paddle motion internally, but gets updates on the other paddle motion from the server.

I think that I'll hold off on that and wait to implement the whole game in PBP. Then, re-address the latency optimization issues once I see how the whole thing feels.

The next thought that comes to mind is maybe just to wrap the Claude-generated server code into a PBP part. Maybe rewrite that code in `.rt`, then get Claude to learn `.rt` syntax?

The first thing in the code that I see is a conventional hard-coded timer call. That should be refactored out as a separate PBP part. Maybe that's a place to start chipping away at refactoring all of the server logic into PBP parts? Or, maybe I will see more disagreeable stuff in the `pong-server.js` code that I will want to change?