from App.extensions import (db, UserMixin, Column,
                            String, Integer, ForeignKey, Text, datetime, ma)


class Innovation(db.Model, UserMixin):
    """This class defines the Category fields in the database"""
    __tablename__ = "innovations"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text(), nullable=False)
    image_url = Column(String(60), nullable=False)
    created_on = Column(String, nullable=True, default=datetime.now)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    def __init__(self, name, description, image_url, user_id, category_id):
        """This defines the init method
        Parameters:
            name (string): The user name
            description (strin): the user description
            image_url (string): The image_url of the Innovation
            user_id (int): User user_id
            category_id (int): category of the innovation
        """
        self.name = name
        self.description = description
        self.image_url = image_url
        self.user_id = user_id
        self.category_id = category_id

    def inser(self):
        """This function insert new categInnovationory into the database"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """This function update Innovation details in the database"""
        db.session.update(self)

    def delete(self):
        """This function delete innovation from the database"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """This function defines innovation representation object"""
        return f"Innovation({self.name}, {self.description}, {self.created_on})"


class InnovationSchema(ma.Schema):
    """This class defines the innovation schema for fetching data"""
    class Meta:
        fields = ('id', 'Title', 'description', 'image_url',
                  'created_on', 'username', 'Category Name')
        model = Innovation


# Instantiating the category schema
innovation_schema = InnovationSchema()
innovations_schema = InnovationSchema(many=True)
