from App.extensions import (
    db, UserMixin, ma, Column, String, Integer, relationship, datetime)


class Category(db.Model, UserMixin):
    """This class defines the Category fields in the database"""
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_on = Column(String, nullable=True, default=datetime.now)
    innovation = relationship("Innovation", backref="category", lazy=True)

    def __init__(self, name):
        """This function defines the contructor of the category class
        Paramenter:
            name (string): category name
        """
        self.name = name

    def insert(self):
        """This function insert new category into the database"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """This function update category details in the database"""
        db.session.commit(self)

    def delete(self):
        """This function delete category from the database"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """This function defines category representation object"""
        return f"Category({self.name} created on {self.created_on})"


class CategorySchema(ma.Schema):
    """This class defines the Category schema for fetching data"""
    class Meta:
        fields = ('id', 'name', 'created_on')
        model = Category


# Instantiating the category schema
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
