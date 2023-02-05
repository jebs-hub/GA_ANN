from env.env import Environment
env = Environment(500,2000,10,10,70)

def build():
    env.model.start_gen()
    env.create_view()
    env.run_simulation()
    env.model.end_simulation()
    env.model.rank()
    env.model.print_gen_report()
    env.model.save_report(n=10)

def rebuild():
    env.model.rebuild_gen("gen0")
    env.create_view()
    env.run_simulation()
    env.model.print_gen_report()

rebuild()