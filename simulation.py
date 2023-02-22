from env.env import Environment
env = Environment(500,3000,5,10,70)

def build():
    env.model.start_gen()
    env.create_view()
    env.run_simulation()
    env.model.end_simulation()
    env.model.rank()
    env.model.print_gen_report()
    env.model.print_orgs_report(n=10)
    #env.model.save_report(n=10)


def rebuild():
    env.model.rebuild_gen("train3/gen0",1)
    env.create_view()
    env.run_simulation()
    env.model.print_gen_report()


rebuild()