from typing import List, Dict, Any, Optional, Union, Callable, Type
from abc import ABC, abstractmethod

class Command(ABC):

    name: str = ""
    min_args: int = 0
    max_args: Optional[int] = None
    description: str = ""

    def __init__(self, db):
        """Initializes with a reference to the database"""
        self.db = db

    @abstractmethod
    def execute(self, args: List[str]) -> str:
        """Executes the command with the given arguments"""
        pass

    def validate_args(self, args: List[str]) -> Optional[str]:
        """
        Validates the number of arguments.

        Args:
            args: List -> List with the arguments for the command
        
        Returns:
            None if valid, error message if invalid
        """
        if len(args) < self.min_args:
            return f"ERROR: {self.name} command requires at least {self.min_args} argument(s)"
        
        if self.max_args is not None and len(args) > self.max_args:
            return f"ERROR: {self.name} command takes at most {self.max_args} argument(s)"
        
        return None


class CommandRegistry:

    def __init__(self,db) -> None:
        """Initializes the registry with a database reference"""
        self.db = db
        self.commands = Dict[str,Command] = {}

    def register(self, command_class: Type[Command]) -> None:
        """Registers the command class"""
        command = command_class(self.db)
        self.commands[command.name] = command

    def register_all(self, command_classes: List[Type[Command]]) -> None:
        """Registers multiple command classes at once"""
        for command_class in command_classes:
            self.register(command_class)

    def get_command(self, name: str) -> Optional[Command]:
        """Get a command by name."""
        return self.commands.get(name.upper())
    
    def get_all_commands(self) -> Dict[str, Command]:
        """Get all the registered commands."""
        return self.commands
    

class SetCommand(Command):
    """Way to SET the key-value pair in the database"""

    name = "SET"
    min_args = 2
    max_args = 6
    description = "Set key to hold the value field. If key exists, it is overwritten."

    def execute(self, args: List[Any]) -> str:
        error = self.validate_args(args)

        if error:
            return error
        
        key, value = args[0], args[1]

        ttl = None
        nx = False
        xx = False

        i = 2
        while i < len(args):
            if args[i].upper() == "EX" and i + 1 < len(args):
                try:
                    ttl = int(args[i+1])
                    i = i + 2
                except ValueError:
                    return "ERROR: EX value must be an integer"
                
            elif args[i].upper() == "EX":
                nx = True
                i = i + 1

            elif args[i].upper() == "XX":
                xx = True
                i += 1

            else:
                return f"ERROR: Invalid option '{args[i]}'"

        # Checking for clashing config 
        if nx and xx:
            return "ERROR: NX and XX options cannot be used together"
        
        result = self.db.set(
            key,
            value,
            ttl,
            nx,
            xx
        )

        if result is None:
            return "Not Found"
        
        return "OK"
    

class GetCommand(Command):
    """GET command used to fetch the key-value pair"""
    
    name = "GET"
    min_args = 1
    max_args = 1
    description = "Get the value of key. If the key does not exist, return Not Found."
    
    def execute(self, args: List[str]) -> str:
        error = self.validate_args(args)
        
        if error:
            return error
        
        value = self.db.get(args[0])
        
        if value is None:
            return "Not Found"
        
        return str(value)


class DelCommand(Command):
    """DEL command used to delete the value with the specified key"""
    
    name = "DEL"
    min_args = 1
    description = "Remove specified keys. Returns the number of keys removed."
    
    def execute(self, args: List[str]) -> str:
        error = self.validate_args(args)

        if error:
            return error
        
        deleted = 0
        
        for key in args:
            if self.db.delete(key):
                deleted += 1
        
        return str(deleted)


class ExistsCommand(Command):
    """EXISTS command used to check how many of the keys exists in the database"""
    
    name = "EXISTS"
    min_args = 1
    description = "Check if keys exist. Returns number of existing keys."
    
    def execute(self, args: List[str]) -> str:
        error = self.validate_args(args)
        if error:
            return error
        
        count = 0
        for key in args:
            if self.db.exists(key):
                count += 1
        
        return str(count)


class ExpireCommand(Command):
    """EXPIRE Command used to set a timeout against the key"""
    
    name = "EXPIRE"
    min_args = 2
    max_args = 2
    description = "Set a timeout on key in seconds. Return 1 if set, 0 if not."
    
    def execute(self, args: List[str]) -> str:
        error = self.validate_args(args)

        if error:
            return error
        
        key = args[0]
        try:
            seconds = int(args[1])
        except ValueError:
            return "ERROR: Seconds must be an integer"
        
        result = self.db.expire(key, seconds)
        return "1" if result else "0"


class TtlCommand(Command):
    """TTL Command used to check the remaining amount of time left to live for a particular key"""
    
    name = "TTL"
    min_args = 1
    max_args = 1
    description = "Get remaining time to live of a key in seconds."
    
    def execute(self, args: List[str]) -> str:
        error = self.validate_args(args)

        if error:
            return error
        
        return str(self.db.ttl(args[0]))


class AppendCommand(Command):
    """APPEND Command used to add a value to the values associated with the key"""
    
    name = "APPEND"
    min_args = 2
    max_args = 2
    description = "Append value to key. Creates the key if it doesn't exist."
    
    def execute(self, args: List[str]) -> str:
        error = self.validate_args(args)

        if error:
            return error
        
        key, value = args[0], args[1]
        return str(self.db.append(key, value))


class KeysCommand(Command):
    """KEYS Command used to find all the keys that match the provided pattern"""
    
    name = "KEYS"
    min_args = 1
    max_args = 1
    description = "Find all keys matching the given pattern."
    
    def execute(self, args: List[str]) -> str:
        error = self.validate_args(args)

        if error:
            return error
        
        pattern = args[0]
        keys = self.db.keys(pattern)
        
        if not keys:
            return "Not Found"
        
        return "\n".join([f"{i+1}) {key}" for i, key in enumerate(keys)])


class FlushDBCommand(Command):
    """FLUSHDB Command to remove all the keys from the existing database"""
    
    name = "FLUSHDB"
    max_args = 0
    description = "Remove all keys from the current database."
    
    def execute(self, args: List[str]) -> str:
        error = self.validate_args(args)

        if error:
            return error
        
        self.db.flushdb()
        return "OK"


class InfoCommand(Command):
    """INFO Command that will be used to give all information regarding the database server"""
    
    name = "INFO"
    max_args = 1
    description = "Get information and statistics about the server."
    
    def execute(self, args: List[str]) -> str:
        error = self.validate_args(args)

        if error:
            return error
        
        section = args[0] if args else None
        info = self.db.info(section)
        
        if not info:
            return "(no information available)"
        
        output = []

        for key, value in info.items():
            output.append(f"{key}: {value}")

        return "\n".join(output)


class MultiCommand(Command):
    """MULTI command that will start the transaction"""
    
    name = "MULTI"
    max_args = 0
    description = "Mark the start of a transaction block."
    
    def execute(self, args: List[str]) -> str:
        error = self.validate_args(args)

        if error:
            return error
        
        if self.db.start_transaction():
            return "OK"
        
        return "ERROR: Transaction already in progress"


class ExecCommand(Command):
    """EXEC Command helps execute all the commands after the transaction is initiated"""
    
    name = "EXEC"
    max_args = 0
    description = "Execute all commands issued after MULTI."
    
    def execute(self, args: List[str]) -> str:
        error = self.validate_args(args)

        if error:
            return error
        
        results = self.db.exec_transaction()

        if results is None:
            return "ERROR: No transaction in progress"
        
        if not results:
            return "(empty transaction)"
        
        return "\n".join([f"{i+1}) {result}" for i, result in enumerate(results)])


class DiscardCommand(Command):
    """DISCARD Command deletes all the commands initiated in the transaction"""
    
    name = "DISCARD"
    max_args = 0
    description = "Discard all commands issued after MULTI."
    
    def execute(self, args: List[str]) -> str:
        error = self.validate_args(args)

        if error:
            return error
        
        if self.db.discard_transaction():
            return "OK"
        
        return "ERROR: No transaction in progress"
    

class CommandFactory:
    """Factory for creating and registering all available commands."""
    
    @staticmethod
    def create_all_commands() -> List[Type[Command]]:
        """Get a list of all available command classes."""
        return [
            SetCommand,
            GetCommand,
            DelCommand,
            ExistsCommand,
            ExpireCommand,
            TtlCommand,
            
            AppendCommand,
            KeysCommand,
            FlushDBCommand,
            InfoCommand,
            
            MultiCommand,
            ExecCommand,
            DiscardCommand,
        ]