####
##
## URUGUAY's personal information VALIDATORS
##
## You can use this validators tu check if user input is
## a valid uruguayan:
##   * personal identificator: ci_validator
##   * company identificator: rut_validator
##   * mobilephone number: mobilephone_validator
##   * telephone number: telephone_validator
##
##
## Created by: 
##    * Luis Lopez <luislopez72@gmail.com>
##
####

from django.core.exceptions import ValidationError
import os
import re
import logging

logger = logging.getLogger('django')


def clean_int(data):
    """
    Devuelve solo los caracteres numericos de un string 
    """
    return re.sub(r'[^0-9]', '', str(data))


def cedula_uy(documento):
    """
    Valida si una cedula de identidad uruguaya es correcta
    """
    documento = clean_int(documento)  # Nos quedamos solo con los numeros
    if len(documento) in [6,7,8]:
        documento = '0' * (8 - len(documento)) + documento  # Dejamos el documento con 8 caracteres
        lst_doc = list(documento)  # Vamos a necesitar una lista
        dv = int(lst_doc.pop())  # Asumimos que el dig. verificador es el ultimo numero
        
        # Calculamos nosotros el dig. verificador por separado
        factores = [2,9,8,7,6,3,4]
        sumatoria = 0
        for d in range(0,7):
            sumatoria += int(lst_doc[d]) * factores[d]
        x = (sumatoria % 10)
        _dv = 0 if x == 0 else 10 - x

        if dv == _dv:
            return True
    return False


def rut_uruguay(numero):
    """
    Valida si un RUT/RUC uruguayo es correcto
    """
    n = clean_int(numero) # Nos quedamos solo con los numeros
    if len(n) != 12:
        return False

    dc = int(n[-1:])  # El ultimo digito sera nuestro verificador
    rut = list(n[0:11])
    total = 0
    factor = 2
    operaciones = list()

    # Iteramos sobre cada elemento (pero de derecha a izquierda)
    for i in reversed(rut):
        total += factor * int(i)
        operaciones.append('%s*%i' % (i, factor))
        if factor == 9:
            factor = 2
        else:
            factor += 1

    dv = 11 - (total % 11)
    if dv == 11:
        dv = 0
    elif dv == 10:
        dv = 1
    return dv == dc


def celular_uy(numero):
    """
    Valida si un numero de celular es correcto
    """
    n = clean_int(numero)  # Nos quedamos solo con los numeros
    if re.match(r'0?9[0-9]{7}', n) is not None:
        return True
    return False


def telefono_uy(numero):
    """
    Valida si un numero de telefono fijo es correcto
    """
    n = clean_int(numero)  # Nos quedamos solo con los numeros
    if re.match(r'[24][0-9]{7}', n) is not None:
        return True
    return False




##
## Validadores
##

def ci_validator(document):
    dc = str(clean_int(document))
    if len(str(dc)) not in [6, 7, 8]:
        raise ValidationError('CI: El largo del documento NO es valido. %s (#%s)' % (dc, len(dc)))
    if not cedula_uy(document):
        raise ValidationError('El documento %s NO es un documento uruguayo valido' % str(document))


def rut_validator(number):
    if not rut_uruguay(number):
        raise ValidationError('El RUT ingresado no es un RUT uruguayo valido: %s' % str(number))


def mobilephone_validator(number):
    if not celular_uy(number):
        raise ValidationError('El numero de celular NO es un numero uruguayo valido: %s' % str(number))


def telephone_validator(number):
    if not telefono_uy(number):
        raise ValidationError('El numero de telefono NO es un numero uruguayo valido: %s' % str(number))
