class Script():
    
    def __init__(self, name, instructions):
        self.name = name
        self.instructions = instructions
        
    def __str__(self):
        return '\n'.join(self.instructions)
        
    def __repr__(self):
        return 'Script name: {name}\nCommands:\n{instructions}'\
                            .format(
                                    name = self.name,
                                    instructions = '\n'.join(self.instructions)
                                    )
                   