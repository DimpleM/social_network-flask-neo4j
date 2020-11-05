from py2neo import Graph, Node, Relationship
from passlib.hash import bcrypt
from datetime import datetime
import uuid
import json

graph = Graph()

class User:
    def __init__(self, username):
        self.username = username

    def find(self):
        query = "MATCH (user)  Where user.username = '{0}' RETURN user.username AS username, user.password as password LIMIT 1".format(self.username)
        return graph.run(query).data()

    def register(self, password):
        if not self.find():
            user = Node("User", username=self.username, password=bcrypt.encrypt(password))
            graph.create(user)
            return True
        else:
            return False

    def verify_password(self, password):
        user = self.find()
        if user:
            user = user[0]
        if user:
            return bcrypt.verify(password, user['password'])
        else:
            return False

    def add_post(self, title, content, image, date_posted):
        # user = self.find()
        query = "MATCH (user)  Where user.username = '{0}' RETURN user LIMIT 1".format(self.username)
        user = graph.run(query).data()[0]['user']
        post = Node(
            "Post",
            id=str(uuid.uuid4()),
            title=title,
            content=content,
            date_posted=date_posted,
            image=image
        )
        trans = graph.begin()
        rel = Relationship(user, "PUBLISHED", post)
        trans.create(rel)
        trans.commit()

    def get_posts():
        query = """
        MATCH (user:User)-[:PUBLISHED]->(post:Post)
        RETURN user.username AS username, post
        ORDER BY post.date_posted DESC 
        """
        result = graph.run(query)
        return result.data()