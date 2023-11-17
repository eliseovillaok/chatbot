% Definimos la distancia maxima la cual
% consideramos que dos ciudades son cercanas (EN KILOMETROS)
distancia_maxima(200).

% Formula de la formula de haversine para calcular la distancia entre dos puntos geograficos
% Declaramos las ciudades
es_ciudad('buenos aires').
es_ciudad('la plata').
es_ciudad('mar del plata').
es_ciudad('bahia blanca').
es_ciudad('pilar').
es_ciudad('tigre').
es_ciudad('tandil').
es_ciudad('necochea').
es_ciudad('azul').
es_ciudad('olavarria').
es_ciudad('tres arroyos').
es_ciudad('balcarce').
es_ciudad('chascomus').
es_ciudad('pinamar').
es_ciudad('villa gesell').
es_ciudad('mar de ajo').
es_ciudad('san clemente del tuyu').
es_ciudad('miramar').

% Declaramos los posibles alojamientos
es_alojamiento('hotel').
es_alojamiento('casa').
es_alojamiento('departamento').
es_alojamiento('resort').
es_alojamiento('hostel').
es_alojamiento('cabaña').
es_alojamiento('villa').
es_alojamiento('pension').
es_alojamiento('motel').
es_alojamiento('crucero').
es_alojamiento('barco').

% Coordenadas geograficas (ciudad, latitud y longitud)
coordenadas('buenos aires',-34.60542114388246,-58.35772151769931).
coordenadas('la plata',-34.9207195085947,-57.953952332795126).
coordenadas('mar del plata',-38.002959425937526,-57.53324279211419).
coordenadas('bahia blanca',-38.71828303005894,-62.26632881076482).
coordenadas('pilar',-34.465871069040716,-58.915878283090585).
coordenadas('tigre',-34.42577265350495,-58.582658257686695).
coordenadas('tandil',-37.32826879983299,-59.13561255480667).
coordenadas('necochea',-38.55490324408082,-58.73773672339904).
coordenadas('azul',-36.77471460618667,-59.85331909907985).
coordenadas('olavarria',-36.89286927702053,-60.3251840935795).
coordenadas('tres arroyos',-38.37733715811456, -60.27602770936231).
coordenadas('balcarce',-37.845938052270974, -58.25210597613362).
coordenadas('chascomus',-35.57694637963647, -58.01027302389956).
coordenadas('pinamar',-37.11479118833701, -56.86054616005097).
coordenadas('villa gesell',-37.25945203016066, -56.969160910622264).
coordenadas('mar de ajo',-36.72346681398068, -56.67562745905709).
coordenadas('san clemente del tuyu',-36.57747266485429, -56.6873581333666).
coordenadas('miramar',-38.270291634301785, -57.8403735582475).


% CIUDADES CON PLAYA
tiene_playa('mar del plata').
tiene_playa('necochea').
tiene_playa('pinamar').
tiene_playa('villa gesell').
tiene_playa('mar de ajo').
tiene_playa('san clemente del tuyu').
tiene_playa('miramar').

% CIUDADES CON SIERRAS
tiene_sierras('tandil').
tiene_sierras('azul').
tiene_sierras('olavarria').
tiene_sierras('balcarce').

% DISTANCIA ENTRE DOS CIUDADES -> Distancia
distancia_ciudades(Ciudad1, Ciudad2, Distancia) :-
    es_ciudad(Ciudad1),
    es_ciudad(Ciudad2),
    coordenadas(Ciudad1, Latitud1, Longitud1),
    coordenadas(Ciudad2, Latitud2, Longitud2),
    haversine(Latitud1, Longitud1, Latitud2, Longitud2, Distancia).

% Regla para determinar si dos ciudades son cercanas (dependiendo de la
% distancia maxima definida al principio del archivo)
son_cercanas(Ciudad1, Ciudad2) :-
    distancia_maxima(DistanciaMaxima),
    distancia_ciudades(Ciudad1, Ciudad2, Distancia),
    Distancia =< DistanciaMaxima.






