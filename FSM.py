from random import random
class FSM:

    def __init__(self):

        # initializing states
        self.sleep_st = self._create_sleep()
        self.wake_up_st = self._create_wake_up()
        self.breakfast_st = self._create_breakfast()
        self.decide_what_to_do_st = self._create_decide_what_to_do()
        self.study_at_ucu_st = self._create_study_at_ucu()
        self.eat_at_ucu_st = self._create_eat_at_ucu()
        self.walk_st = self._create_walk()
        self.less_tired_at_home_st = self._create_less_tired_at_home()
        self.run_st = self._create_run()
        self.tired_at_home_st = self._create_tired_at_home()
        self.study_at_home_st = self._create_study_at_home()
        self.eat_at_home_st = self._create_eat_at_home()

        # probing
        next(self.sleep_st)
        next(self.wake_up_st)
        next(self.breakfast_st)
        next(self.decide_what_to_do_st)
        next(self.study_at_ucu_st)
        next(self.eat_at_ucu_st)
        next(self.walk_st)
        next(self.less_tired_at_home_st)
        next(self.run_st)
        next(self.tired_at_home_st)
        next(self.study_at_home_st)
        next(self.eat_at_home_st)

    
        # setting current state of the system
        self.__awake = 14
        self.__hunger = 0
        self.state = self.sleep_st

    def send(self, char):
        self.state.send(char)


    def update_stats(self):
        self.__awake += 1
        self.__hunger += 1
    def hungry(self):
        return self.__hunger >= 5
    def eat(self):
        self.__hunger = 0
    def get_tired(self):
        self.__awake += 2
    def sleepy(self):
        return self.__awake >= 15
    def rested(self):
        return self.__awake < 1
    def sleep(self):
        self.__awake -= 2
    def show_stats(self):
        """
        return hunger, awake
        """
        return self.__hunger, self.__awake

    def _create_sleep(self):
        while True:
            hour = yield
            if not self.rested():
                self.sleep()
                self.state = self.sleep_st
            elif self.rested():
                self.state = self.wake_up_st
                self.update_stats()

    def _create_wake_up(self):
        while True:
            hour = yield
            self.update_stats()
            self.state = self.breakfast_st

    def _create_breakfast(self):
        while True:
            hour = yield
            self.eat()
            self.update_stats()
            self.state = self.decide_what_to_do_st

    def _create_decide_what_to_do(self):
        while True:
            hour = yield
            rand = random()
            self.update_stats()
            if rand > 0.3 and self.state == self.decide_what_to_do_st and 8 < hour < 20:
                self.state = self.study_at_ucu_st
            elif self.state == self.decide_what_to_do_st:
                self.state = self.study_at_home_st

    def _create_study_at_ucu(self):
        while True:
            hour = yield
            self.update_stats()
            if random() > 0.5 and hour == 21:
                self.state = self.walk_st
            elif hour == 22:
                self.state = self.run_st
            elif self.hungry() and hour < 19:
                self.state = self.eat_at_ucu_st
            else:
                self.state = self.study_at_ucu_st

    def _create_eat_at_ucu(self):
        while True:
            hour = yield
            self.update_stats()
            if random() > 0.5 and hour == 21:
                self.state = self.walk_st
            elif hour == 22:
                self.state = self.run_st
            else:
                self.eat()
                self.state = self.study_at_ucu_st
            
    def _create_walk(self):
        while True:
            hour = yield
            self.update_stats()
            self.state = self.less_tired_at_home_st

    def _create_less_tired_at_home(self):
        while True:
            hour = yield
            rand = random()
            self.update_stats()
            if rand > (0.66 * (16/self.__awake)) and self.sleepy():
                self.state = self.sleep_st
            else:
                self.state = self.less_tired_at_home_st

    def _create_run(self):
        while True:
            hour = yield
            self.update_stats()
            self.state = self.tired_at_home_st

    def _create_tired_at_home(self):
        while True:
            hour = yield
            self.get_tired()
            self.update_stats()
            self.state = self.less_tired_at_home_st

    def _create_study_at_home(self):
        while True:
            hour = yield
            self.update_stats()
            if self.hungry():
                self.state = self.eat_at_home_st
            elif self.sleepy():
                self.state = self.less_tired_at_home_st
            else:
                self.state = self.study_at_home_st

    def _create_eat_at_home(self):
        while True:
            hour = yield
            self.eat()
            if self.sleepy():
                self.state = self.tired_at_home_st
            else:
                self.state = self.study_at_home_st

def run_24_hour_loop(me: FSM):
    for hour in range(24):
        print('\t', f"{hour}:00".rjust(5, "0"), '\t', me.state.__name__[8:], end= " -> ")
        me.send(hour)
        print(me.state.__name__[8:])

def main():
    me = FSM()
    for day in range(28):
        print(f"day {day}")
        run_24_hour_loop(me)

if __name__ == "__main__":
    main()
