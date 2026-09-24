from django.db import models

class WasteImage(models.Model):
    image = models.ImageField(upload_to='waste_ml/waste_images/')
    prediction = models.CharField(max_length=50, blank=True)
    confidence = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.prediction or "No prediction"

    
