from main_app.models import *
from django import forms
from PIL import Image

# Create your models here.

def validate_input(inp):
    if inp<=0:
        raise forms.ValidationError('Negative Values are not allowed!!!')

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default="test.jpg",upload_to="user_pics")
    plan = models.ForeignKey(PlanCategory,on_delete=models.CASCADE,null=True)
    height = models.DecimalField(max_digits=5,decimal_places=2,validators=[validate_input],null=True)
    weight = models.DecimalField(max_digits=5,decimal_places=2,validators=[validate_input],null=True)
    gender = models.CharField(max_length=10,null=True)
    age = models.IntegerField(validators=[validate_input],null=True)
    lifestyle = models.CharField(max_length=50,null=True)
    calorie_goal = models.CharField(max_length=20,null=True)
    ideal_wt = models.CharField(max_length=30,null=True)
    target_wt = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.user.username}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)

        img = Image.open(self.image.path)

        if img.height>300 or img.width>300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
