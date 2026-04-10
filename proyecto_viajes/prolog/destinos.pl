/* ========================================
BASE PARA LA PLANIFICACION DE VIAJES GLOBALES
Proyecto de Lenguajes y Paradigmas de Programacion
Equipo: Kendal, Eugene, Berny, Kate
======================================== */

/* Declaraciones dinamicas - permiten retract y assert */
:- dynamic visitado/1.
:- dynamic continente_visitado/1.
:- dynamic gusto/1.
:- dynamic presupuesto_usuario/1.
:- dynamic clima_preferido/1.
:- dynamic tipoviaje_preferido/1.

/* CONTINENTES */
continente(america).
continente(europa).
continente(asia).
continente(africa).
continente(oceania).

/* TIPOS DE DESTINO */
tipodestino(playa).
tipodestino(montana).
tipodestino(ciudad).
tipodestino(cultural).
tipodestino(naturaleza).
tipodestino(aventura).

/* COSTOS */
costo(bajo).
costo(medio).
costo(alto).

/* CLIMAS */
clima(tropical).
clima(templado).
clima(frio).
clima(desertico).

/* EXPERIENCIAS */
experiencia(gastronomia).
experiencia(historia).
experiencia(vidanocturna).
experiencia(ecoturismo).
experiencia(aventura).
experiencia(tecnologia).
experiencia(relajacion).

/* AMERICA */
destino(nicaragua, america, espanol, naturaleza, bajo, tropical, aventura).
destino(nicaragua, america, espanol, cultural, bajo, tropical, historia).
destino(guatemala, america, espanol, cultural, bajo, templado, historia).
destino(guatemala, america, espanol, naturaleza, bajo, templado, aventura).
destino(honduras, america, espanol, playa, bajo, tropical, ecoturismo).
destino(honduras, america, espanol, naturaleza, bajo, tropical, aventura).
destino(el_salvador, america, espanol, playa, bajo, tropical, relajacion).
destino(belice, america, ingles, naturaleza, medio, tropical, ecoturismo).
destino(cuba, america, espanol, playa, bajo, tropical, relajacion).
destino(colombia, america, espanol, playa, medio, tropical, vidanocturna).
destino(brasil, america, portugues, playa, medio, tropical, vidanocturna).
destino(peru, america, espanol, cultural, medio, templado, historia).
destino(peru, america, espanol, aventura, medio, templado, aventura).
destino(argentina, america, espanol, ciudad, medio, templado, vidanocturna).
destino(chile, america, espanol, naturaleza, medio, frio, aventura).
destino(mexico, america, espanol, cultural, medio, tropical, gastronomia).
destino(canada, america, ingles, naturaleza, alto, frio, ecoturismo).
destino(estados_unidos, america, ingles, ciudad, alto, templado, vidanocturna).

/* EUROPA */
destino(espana, europa, espanol, playa, medio, templado, vidanocturna).
destino(portugal, europa, portugues, playa, medio, templado, gastronomia).
destino(grecia, europa, griego, playa, medio, templado, historia).
destino(italia, europa, italiano, cultural, alto, templado, gastronomia).
destino(francia, europa, frances, cultural, alto, templado, gastronomia).
destino(alemania, europa, aleman, ciudad, medio, templado, historia).
destino(austria, europa, aleman, cultural, medio, templado, historia).

/* ASIA */
destino(tailandia, asia, tailandes, playa, bajo, tropical, gastronomia).
destino(vietnam, asia, vietnamita, cultural, bajo, tropical, historia).
destino(indonesia, asia, indonesio, playa, bajo, tropical, naturaleza).
destino(india, asia, hindi, cultural, bajo, tropical, historia).
destino(malasia, asia, malayo, naturaleza, medio, tropical, ecoturismo).
destino(japon, asia, japones, cultural, alto, templado, tecnologia).
destino(china, asia, chino, cultural, medio, templado, historia).
destino(nepal, asia, nepali, montana, bajo, frio, aventura).

/* AFRICA */
destino(marruecos, africa, arabe, cultural, medio, desertico, historia).
destino(egipto, africa, arabe, cultural, medio, desertico, historia).
destino(kenia, africa, ingles, naturaleza, medio, tropical, ecoturismo).
destino(tanzania, africa, suajili, naturaleza, medio, tropical, aventura).
destino(sudafrica, africa, ingles, naturaleza, medio, templado, ecoturismo).

/* OCEANIA */
destino(australia, oceania, ingles, naturaleza, alto, templado, aventura).
destino(nueva_zelanda, oceania, ingles, naturaleza, alto, templado, aventura).
destino(fiyi, oceania, ingles, playa, medio, tropical, relajacion).

/* ========================================
PERFIL DEL VIAJERO - datos de ejemplo
======================================== */
visitado(costa_rica).
visitado(panama).
visitado(mexico).

continente_visitado(america).

gusto(gastronomia).
gusto(historia).
gusto(ecoturismo).
gusto(aventura).

presupuesto_usuario(medio).
clima_preferido(tropical).
tipoviaje_preferido(cultural).

/* ========================================
REGLAS
======================================== */

/* Regla de presupuesto compatible */
presupuesto_compatible(bajo, bajo).
presupuesto_compatible(medio, bajo).
presupuesto_compatible(medio, medio).
presupuesto_compatible(alto, bajo).
presupuesto_compatible(alto, medio).
presupuesto_compatible(alto, alto).

presupuesto_aceptable(Destino) :-
    destino(Destino, _, _, _, Costo, _, _),
    presupuesto_usuario(Presupuesto),
    presupuesto_compatible(Presupuesto, Costo).

/* Pais no visitado */
no_visitado(Destino) :-
    destino(Destino, _, _, _, _, _, _),
    \+ visitado(Destino).

/* Coincide con clima */
coincide_clima(Destino) :-
    destino(Destino, _, _, _, _, Clima, _),
    clima_preferido(Clima).

/* Coincide con gustos */
coincide_gusto(Destino) :-
    destino(Destino, _, _, _, _, _, Experiencia),
    gusto(Experiencia).

/* RECOMENDACION PRINCIPAL */
recomendado(Destino) :-
    no_visitado(Destino),
    presupuesto_aceptable(Destino),
    coincide_clima(Destino),
    coincide_gusto(Destino).

/* DESTINO DIFERENTE */
continente_nuevo(Destino) :-
    destino(Destino, Continente, _, _, _, _, _),
    \+ continente_visitado(Continente).

experiencia_nueva(Destino) :-
    destino(Destino, _, _, _, _, _, Experiencia),
    \+ gusto(Experiencia).

destino_diferente(Destino) :-
    no_visitado(Destino),
    presupuesto_aceptable(Destino),
    (continente_nuevo(Destino) ; experiencia_nueva(Destino)).