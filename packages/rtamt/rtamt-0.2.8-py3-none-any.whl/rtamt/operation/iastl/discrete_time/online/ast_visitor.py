from rtamt.operation.stl.discrete_time.online.ast_visitor import StlDiscreteTimeOnlineAstVisitor
from rtamt.operation.iastl.discrete_time.online.predicate_operation import PredicateOperation
from rtamt.enumerations.options import Semantics

class IAStlOutputRobustnessDiscreteTimeOnlineAstVisitor(StlDiscreteTimeOnlineAstVisitor):

    def visitPredicate(self, node, *args, **kwargs):
        self.visitChildren(node, *args, **kwargs)
        self.online_operator_dict[node.name] = PredicateOperation(node.operator, Semantics.OUTPUT_ROBUSTNESS,
                                                                  node.in_vars, node.out_vars)

class IAStlInputVacuityDiscreteTimeOnlineAstVisitor(StlDiscreteTimeOnlineAstVisitor):

    def visitPredicate(self, node, *args, **kwargs):
        self.visitChildren(node, *args, **kwargs)
        self.online_operator_dict[node.name] = PredicateOperation(node.operator, Semantics.INPUT_VACUITY,
                                                                  node.in_vars, node.out_vars)

class IAStlOutputVacuityDiscreteTimeOnlineAstVisitor(StlDiscreteTimeOnlineAstVisitor):

    def visitPredicate(self, node, *args, **kwargs):
        self.visitChildren(node, *args, **kwargs)
        self.online_operator_dict[node.name] = PredicateOperation(node.operator, Semantics.OUTPUT_VACUITY,
                                                                  node.in_vars, node.out_vars)

class IAStlOutputRobustnessDiscreteTimeOnlineAstVisitor(StlDiscreteTimeOnlineAstVisitor):

    def visitPredicate(self, node, *args, **kwargs):
        self.visitChildren(node, *args, **kwargs)
        self.online_operator_dict[node.name] = PredicateOperation(node.operator, Semantics.OUTPUT_ROBUSTNESS,
                                                                  node.in_vars, node.out_vars)