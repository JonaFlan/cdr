from datetime import datetime, timedelta
from django.utils.timezone import now
from core.models import Prestamo

def liberar_juegos_no_retirados():
    """Libera juegos que no fueron retirados el mismo día."""
    reservas_vencidas = Prestamo.objects.filter(
        estado='RESERVADO',
        fecha_reserva__lt=now() - timedelta(days=1)  # Más de un día desde la reserva.
    )
    for prestamo in reservas_vencidas:
        prestamo.juego.estado = 'DISPONIBLE'
        prestamo.juego.save()
        prestamo.estado = 'FINALIZADO'
        prestamo.save()
        print(f"Juego liberado: {prestamo.juego.nombre} (ID: {prestamo.juego.id})")