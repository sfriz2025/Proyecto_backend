from App.domain.cuentas_domain import Cuenta
from App.infrastructure.models import CuentaModel


def cuenta_a_dominio(modelo: CuentaModel) -> Cuenta:
    return Cuenta(
        id=modelo.id,
        nombre_titular=modelo.nombre_titular,
        correo=modelo.correo,
        presupuesto_mensual=modelo.presupuesto_mensual,
        fecha_creacion=modelo.fecha_creacion,
    )


def cuenta_a_modelo(cuenta: Cuenta) -> CuentaModel:
    return CuentaModel(
        id=cuenta.id if cuenta.id > 0 else None,
        nombre_titular=cuenta.nombre_titular,
        correo=cuenta.correo,
        presupuesto_mensual=cuenta.presupuesto_mensual,
        fecha_creacion=cuenta.fecha_creacion,
    )
