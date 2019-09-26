# Data
import json

class Maze(object):
    def __init__(self, height = 0, width = 0):
        self.height = height
        self.width = width

    def grid(self):
        return ("%s %s" % (self.height, self.width))
    
    # def theGrid(self):
    #     return "{0} {1}".format(self.height, self.width)

    @classmethod
    def getAll(self):
        database = open('db.txt', 'r')
        result = []
        json_list = json.loads(database.read())
        for item in json_list["item"]:
            # item = json.loads(item)
            maze = Maze(item["height"], item["width"])
            result.append(maze)
        return result

#     #Returns an empty maze of given size
#     def make_empty_maze(width, height):
#         maze = [[[] for b in range(width)] for a in range(height)]
# return maze


# import json

# class Person(object):
#    def __init__(self, first_name = None, last_name = None):
#       self.first_name = first_name
#       self.last_name = last_name
#    #returns Person name, ex: John Doe
#    def name(self):
#       return ("%s %s" % (self.first_name,self.last_name))
		
#    @classmethod
#    #returns all people inside db.txt as list of Person objects
#    def getAll(self):
#       database = open('db.txt', 'r')
#       result = []
#       json_list = json.loads(database.read())
#       for item in json_list["item"]:
#          person = Person(item['first_name'], item['last_name'])
#          result.append(person)
#       return result