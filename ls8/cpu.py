"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8 # R0, R1, R2, R3... R7
        self.pc = 0

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0 # to index into the RAM array

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8  register[0] = 8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0    print(register[0])
            0b00000000,
            0b00000001, # HLT
        ]

        # this adds each instruction in the program to RAM
        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
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
        self.pc = 0
        running = True
        while running:
            ir = self.ram[self.pc]

            operand_a = self.ram_read(self.pc+1) 
            operand_b = self.ram_read(self.pc+2)

            if ir == LDI:
                reg_num = operand_a # self.ram[self.pc+1]
                value = operand_b # self.ram[self.pc+2]
                self.register[reg_num] = value
                self.pc += 3

            elif ir == PRN:
                reg_num = operand_a # self.ram[self.pc+1]
                print(self.register[reg_num])
                self.pc += 2
            elif ir == HLT:
                running = False
                self.pc += 1
            else:
                print(f'Unknown instruction {ir} at address {pc}')
                sys.exit(1)
