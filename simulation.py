from env.env import Environment
env = Environment(500,1,1,10,180)

def build():
    env.model.start_gen()
    env.create_view()
    env.run_simulation()
    env.model.end_simulation()
    #env.model.rank()
    #env.model.print_gen_report()
    #env.model.print_orgs_report(n=10)
    #env.model.save_report(n=10)


def rebuild():
    env.model.rebuild_gen("train10/gen0",1)
    env.create_view()
    env.run_simulation()
    env.model.print_gen_report()


rebuild()