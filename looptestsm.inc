            def enter_idle (): self.state = "idle"
            def step_idle ():
                if x < 0:
                    exit_idle ()
                    enter_wait_for_zero_recrossing ()
                elif x > self.width:
                    exit_idle ()
                    enter_wait_for_w_recrossing ()
                else:
                    Loop ()
            def exit_idle (): pass

            def enter_wait_for_zero_recrossing ():
                zd.send (eh, "rev", "", mev)
                Loop ()
                self.state = "wait for zero re-crossing"
            def step_wait_for_zero_recrossing ():
                if x >= 0:
                    Loop ()
                    exit_wait_for_zero_recrossing ()
                    enter_idle ()
            def exit_wait_for_zero_recrossing (): pass

            def enter_wait_for_w_recrossing ():
                zd.send (eh, "rev", "", mev)
                Loop ()
                self.state = "wait for w re-crossing"
            def step_wait_for_w_recrossing ():
                if x <= self.width:
                    Loop ()
                    exit_wait_for_w_recrossing ()
                    enter_idle ()
            def exit_wait_for_w_recrossing (): pass

            match self.state:
                case "idle":
                    step_idle ()
                case "wait for zero re-crossing":
                    step_wait_for_zero_recrossing ()
                case "wait for w re-crossing":
                    step_wait_for_w_recrossing ()
