
# how to use

jinja_env = jinja2.Environment()
jinja_env.globals["now"] = datetime.datetime.now
jinja_env.add_extension("jinja2.ext.do")

data = {'product':'exceltpl',"version":'0.0.1','terminology':[{'key':'N/A','value':'Not applicable'}]}

doc = xlsxDocument("examples/example.xlsx", data, jinja_env)
doc.render()
doc.save("examples/result.xlsx")
