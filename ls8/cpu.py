"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8 # R0, R1, R2, R3... R7
        self.SP = 7
        self.pc = 0
        self.running = True
        # Branch Table
        self.branch_table = {
            0b00000001: self.HLT, 
            0b10000010: self.LDI, 
            0b01000111: self.PRN,
            0b10100010: self.MUL,
            0b01000101: self.PUSH,

        }

    # Function to call the Branch Table
    def call_bt(self, n, x=None, y=None):
        self.branch_table[n](x, y)

    def LDI(self, reg_num, value):
        self.register[reg_num] = value

    def PRN(self, reg_num, value):
        print(self.register[reg_num])

    def HLT(self, reg_num, value):
        self.running = False

    def MUL(self, reg_a, reg_b):
        self.alu('MUL', reg_a, reg_b)

    def PUSH(self, reg_num, value):
        # decrement SP
        self.register[SP] -= 1
        # get the value we want to store from the register (e.g. in stack.ls8
        # earlier LDI operations would have saved a value to R0 and R1 respectively)
        # now we're taking that value and pushing to stack
        value = self.register[reg_num]
        # figure out where to store it
        new_stack_top = self.register[SP]
        # store the value into RAM at the new top of the stack
        self.ram[reg_num] =  

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""
        
        filename = sys.argv[1]

        # address init at 0 as the memory map in the spec allocates from 0x00
        # (i.e. 0th byte of RAM) upwards for program entries, and from 0xF4
        # (i.e. 244th byte of RAM) downwards for the Stack
        address = 0

        with open(filename) as f:
            for line in f:
                line = line.split("#")

                try:
                    v = int(line[0], 2)
                except ValueError:
                    continue

                self.ram[address] = v

                address += 1 

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # spec outlines R7 is reserved as the Stack Pointer (SP),
        # assign that to 245th byte in RAM as per spec
        self.register[SP] = 0b11110100 # 245th (or 0xF4) byte in RAM
         
        self.pc = 0
        # running = True
        while self.running:
            # ir = self.ram[self.pc]
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc+1) 
            operand_b = self.ram_read(self.pc+2)

            # print(ir)
            # print(operand_a)
            # print(operand_b)

            # Replace the IF-ELSE block with Branch Table
            if ir not in self.branch_table:
                print("some kind of error")

            # AND Masks:
            # Identify the number of operands by isolating first 2 bits 
            num_operands = (ir & 0b11000000) >> 6
            # 1 if this is an ALU operation
            if_alu = (ir & 0b00100000) >> 5

            if num_operands == 2 and if_alu == 0:
                self.call_bt(ir, operand_a, operand_b)
            
            if num_operands == 2 and if_alu == 1:
                self.alu("MUL", operand_a, operand_b)
            
            if num_operands == 1:
                self.call_bt(ir, operand_a)

            if num_operands == 0:
                self.call_bt(ir)

            # increment self.pc
            move_pc = num_operands + 1
            self.pc += move_pc

            # if ir == LDI:
            #     reg_num = operand_a # self.ram[self.pc+1]
            #     value = operand_b # self.ram[self.pc+2]
            #     self.register[reg_num] = value
            #     self.pc += 3

            # elif ir == PRN:
            #     reg_num = operand_a # self.ram[self.pc+1]
            #     print(self.register[reg_num])
            #     self.pc += 2
            # elif ir == HLT:
            #     running = False
            #     self.pc += 1
            # elif ir == MUL:
            #     # self.register[reg_num1] *= self.register[reg_num2]
            #     self.alu("MUL", operand_a, operand_b)
            #     self.pc += 3
            # else:
            #     print(f'Unknown instruction {ir} at address {self.pc}')
            #     sys.exit(1)
