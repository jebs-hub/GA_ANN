from env.env import Environment
env = Environment(500,2000,10,10,70)
env.model.start_gen()
env.create_view()
env.run_simulation()
#env.model.end_simulation()
#env.model.rank()
#env.model.save_report(n=1)
#env.model.rebuild_gen("gen0")
#env.model.run_simulation()
#env.model.print_gen_report()