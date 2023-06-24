from App.extensions import (db, Column, String, Text, ForeignKey,
                            Boolean, Integer, UserMixin, datetime)


class Post(db.Model, UserMixin):
    """A class that defines Blog post"""
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    cat_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    title = Column(String(60), nullable=False, unique=True)
    content = Column(Text, nullable=False)
    is_published = Column(Boolean, default=0)
    min_to_read = Column(Integer, nullable=False)
    post_image = Column(String(120), nullable=False)
    created_on = Column(String, nullable=False, default=datetime.now)

    def __init__(self, user_id, cat_id, title, content, min_to_read, post_image):
        """A method that instantiate the Posts class"""
        self.user_id = user_id
        self.cat_id = cat_id
        self.title = title
        self.content = content
        self.min_to_read = min_to_read
        self.post_image = post_image

    def insert(self):
        """A method that add new post"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """A method that update post"""
        db.session.update(self)

    def delete(self):
        """A method that delete a post"""
        db.session.delete(self)
        db.session.commit()
