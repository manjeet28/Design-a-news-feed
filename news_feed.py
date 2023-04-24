import time
import sys
from datetime import datetime

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.following = []
        self.posts = []

    def follow(self, user):
        self.following.append(user)

    def post(self, text):
        post = Post(text, self)
        self.posts.append(post)
        return post

    def __str__(self):
        return self.username

class Post:
    def __init__(self, text, author):
        self.text = text
        self.author = author
        self.timestamp = time.time()
        self.upvotes = 0
        self.downvotes = 0
        self.comments = []

    def upvote(self):
        self.upvotes += 1

    def downvote(self):
        self.downvotes += 1

    def comment(self, text, author):
        comment = Comment(text, author)
        self.comments.append(comment)
        return comment

    def score(self):
        return self.upvotes - self.downvotes

    def __str__(self):
        return f"{self.author}: {self.text}"

class Comment(Post):
    pass

class NewsFeed:
    def __init__(self, user):
        self.user = user

    def show(self, sort_by="followed"):
        posts = []
        for followed_user in self.user.following:
            posts.extend(followed_user.posts)

        if sort_by == "followed":
            pass
        elif sort_by == "score":
            posts.sort(key=lambda post: post.score(), reverse=True)
        elif sort_by == "comments":
            posts.sort(key=lambda post: len(post.comments), reverse=True)
        elif sort_by == "timestamp":
            posts.sort(key=lambda post: post.timestamp, reverse=True)

        for post in posts:
            print(post)
            print(f"\t{post.upvotes} upvotes, {post.downvotes} downvotes")
            for comment in post.comments:
                print(f"\t{comment}")

def time_ago(timestamp):
    now = time.time()
    diff = now - timestamp
    if diff < 60:
        return f"{int(diff)}s ago"
    elif diff < 3600:
        return f"{int(diff / 60)}m ago"
    elif diff < 86400:
        return f"{int(diff / 3600)}h ago"
    else:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

users = {}
current_user = None

def signup(username, password):
    global users
    if username in users:
        print("Username already taken")
    else:
        user = User(username, password)
        users[username] = user
        print(f"User {username} created")

def login(username, password):
    global users
    global current_user
    if username in users and users[username].password == password:
        current_user = users[username]
        print(f"Logged in as {username}")
    else:
      print("Invalid username or password")

def post(text):
    global current_user
    if current_user:
      post = current_user.post(text)
      print(f"Post created: {post}")
    else:
      print("You must be logged in to post")

def follow(username):
    global current_user
    global users
    if current_user:
      if username in users:
          user_to_follow = users[username]
          current_user.follow(user_to_follow)
          print(f"You are now following {username}")
      else:
          print(f"No such user: {username}")
    else:
      print("You must be logged in to follow")

def upvote(post_id):
    global current_user
    if current_user:
      try:
          post_id = int(post_id)
          post_to_upvote = None
          for followed_user in current_user.following:
              for post in followed_user.posts:
                  if id(post) == post_id:
                      post_to_upvote = post
                      break

          if post_to_upvote:
              post_to_upvote.upvote()
              print(f"Upvoted {post_to_upvote}")
          else:
              print(f"No such post: {post_id}")
      except ValueError:
          print("Invalid post id")
    else:
      print("You must be logged in to upvote")

def downvote(post_id):
    global current_user
    if current_user:
        try:
            post_id = int(post_id)
            post_to_downvote = None
            for followed_user in current_user.following:
                for post in followed_user.posts:
                    if id(post) == post_id:
                        post_to_downvote = post
                        break

            if post_to_downvote:
                post_to_downvote.downvote()
                print(f"Downvoted {post_to_downvote}")
            else:
                print(f"No such post: {post_id}")
        except ValueError:
            print("Invalid post id")
    else:
        print("You must be logged in to downvote")

def main():
    while True:
        command = input('> ')
        args = command.split()
        if not args:
            continue
        if args[0] == 'signup':
            if len(args) == 3:
                signup(args[1], args[2])
            else:
                print('Usage: signup username password')
        elif args[0] == 'login':
            if len(args) == 3:
                login(args[1], args[2])
            else:
                print('Usage: login username password')
        elif args[0] == 'post':
            if len(args) >= 2:
                post(' '.join(args[1:]))
            else:
                print('Usage: post text')
        elif args[0] == 'follow':
            if len(args) == 2:
                follow(args[1])
            else:
                print('Usage: follow username')
        elif args[0] == 'upvote':
            if len(args) == 2:
                upvote(args[1])
            else:
                print('Usage: upvote post_id')
        elif args[0] == 'downvote':
            if len(args) == 2:
                downvote(args[1])
            else:
                print('Usage: downvote post_id')
        elif args[0] == 'exit':
            break
        else:
            print(f'Unknown command: {args[0]}')

if __name__ == '__main__':
    main()