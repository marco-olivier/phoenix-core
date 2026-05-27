"""Intermediate representation for kernel compilation"""
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum

class IRNodeType(Enum):
    FUNCTION = "function"
    BASIC_BLOCK = "basic_block"
    INSTRUCTION = "instruction"
    CONSTANT = "constant"
    VARIABLE = "variable"

@dataclass
class IRNode:
    """Base IR node"""
    node_type: IRNodeType
    children: List['IRNode'] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class IRFunction(IRNode):
    """Function in IR"""
    name: str = ""
    args: List[str] = field(default_factory=list)
    body: List[IRNode] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = IRNodeType.FUNCTION

@dataclass
class IRInstruction(IRNode):
    """Single instruction in IR"""
    opcode: str = ""
    operands: List[Any] = field(default_factory=list)
    result: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = IRNodeType.INSTRUCTION

class IntermediateRepresentation:
    """IR builder and manager"""
    
    def __init__(self):
        self.functions: List[IRFunction] = []
        self.constants: Dict[str, Any] = {}
        self._temp_counter = 0
    
    def create_function(self, name: str, args: List[str]) -> IRFunction:
        """Create new function in IR"""
        func = IRFunction(name=name, args=args)
        self.functions.append(func)
        return func
    
    def add_instruction(self, func: IRFunction, opcode: str, 
                        operands: List[Any], result: Optional[str] = None):
        """Add instruction to function"""
        if result is None:
            result = self._new_temp()
        inst = IRInstruction(opcode=opcode, operands=operands, result=result)
        func.body.append(inst)
        return result
    
    def _new_temp(self) -> str:
        """Generate temporary variable name"""
        self._temp_counter += 1
        return f"%t{self._temp_counter}"
    
    def dump(self) -> str:
        """Dump IR as readable text"""
        lines = []
        for func in self.functions:
            lines.append(f"define {func.name}({', '.join(func.args)})")
            for inst in func.body:
                args = ', '.join(str(a) for a in inst.operands)
                lines.append(f"  {inst.result} = {inst.opcode} {args}")
        return '\n'.join(lines)
