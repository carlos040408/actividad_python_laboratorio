from django.db import models

class PuestoSalud(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    puesto = models.ForeignKey(PuestoSalud, on_delete=models.CASCADE, related_name='usuarios')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.puesto.nombre}"

class PruebaLaboratorio(models.Model):
    TIPO_CHOICES = [
        ('Microbiologia', 'Microbiología (15000)'),
        ('Bacteriologia', 'Bacteriología (25000)'),
        ('Quimica', 'Química (35000)'),
    ]
    TARIFAS = {
        'Microbiologia': 15000,
        'Bacteriologia': 25000,
        'Quimica': 35000,
    }

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pruebas')
    tipo_prueba = models.CharField(max_length=20, choices=TIPO_CHOICES)
    cantidad = models.PositiveIntegerField(default=1)

    @property
    def valor_total(self):
        return self.TARIFAS.get(self.tipo_prueba, 0) * self.cantidad