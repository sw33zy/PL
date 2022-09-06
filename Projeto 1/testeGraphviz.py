from graphviz import Digraph


ole = Digraph(comment='YOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')




ole.node('1', 'King Arthur')
ole.node('2', 'Sir Bedevere the Wise')
ole.node('3', 'Sir Lancelot the Brave')
ole.node('4', 'King ')
ole.node('5', 'Sir ')
ole.node('6', 'Sirina')

ole.edges(['12', '13', '45', '46'])
ole.edge('2', '3', constraint='false')



ole.render('test-output/round-table2.gv', view=True) 
