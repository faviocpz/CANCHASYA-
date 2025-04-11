DROP DATABASE IF EXISTS CanchasYa;
CREATE DATABASE CanchasYa;
USE CanchasYa;
CREATE TABLE TIPO_USUARIO (
  idTipoUsuario int(10) NOT NULL AUTO_INCREMENT, 
  nombre        char(3), 
  PRIMARY KEY (idTipoUsuario));
CREATE TABLE USUARIO (
  idUsuario     int(10) NOT NULL AUTO_INCREMENT, 
  username      varchar(30), 
  contraseña    varchar(30), 
  estado        char(1), 
  idTipoUsuario int(10) NOT NULL, 
  PRIMARY KEY (idUsuario));
CREATE TABLE PERSONA (
  idPersona int(10) NOT NULL AUTO_INCREMENT, 
  apellidos varchar(50), 
  nombres   varchar(50), 
  numdoc    int(12), 
  correo    varchar(30), 
  tel       varchar(9), 
  fecha_reg date, 
  foto      varchar(250), 
  idUsuario int(10) NOT NULL, 
  idTipoDoc int(10) NOT NULL, 
  PRIMARY KEY (idPersona));
CREATE TABLE `PLAN` (
  idPlan int(10) NOT NULL AUTO_INCREMENT, 
  nombre varchar(25), 
  tarifa numeric(5, 2), 
  PRIMARY KEY (idPlan));
CREATE TABLE SUSCRIPCION (
  idSuscripcion int(10) NOT NULL AUTO_INCREMENT, 
  fecha_ini     date, 
  fecha_fin     date, 
  estado        char(1), 
  idUsuario     int(10) NOT NULL, 
  idPlan        int(10) NOT NULL, 
  PRIMARY KEY (idSuscripcion));
CREATE TABLE COMPROBANTE (
  numComprobante int(10) NOT NULL AUTO_INCREMENT, 
  igv            numeric(5, 2), 
  subtotal       numeric(5, 2), 
  total          numeric(5, 2), 
  fecha          date, 
  idSuscripcion  int(10) NOT NULL, 
  idFormaPago    int(10) NOT NULL, 
  PRIMARY KEY (numComprobante));
CREATE TABLE FORMA_PAGO (
  idFormaPago int(10) NOT NULL AUTO_INCREMENT, 
  nombre      varchar(25), 
  estado      char(1), 
  PRIMARY KEY (idFormaPago));
CREATE TABLE LOCAL (
  idLocal    int(10) NOT NULL AUTO_INCREMENT, 
  nombre     varchar(50), 
  direccion  varchar(60), 
  tel        varchar(9), 
  correo     varchar(30), 
  facebook   varchar(30), 
  instagram  varchar(30), 
  puntuacion numeric(4, 2), 
  estado     char(1), 
  idPersona  int(10) NOT NULL, 
  PRIMARY KEY (idLocal));
CREATE TABLE HORARIO_ATENCION (
  idHorario_A int(10) NOT NULL AUTO_INCREMENT, 
  h_inicio    timestamp NULL, 
  h_fin       timestamp NULL, 
  turno       varchar(15), 
  estado      char(1), 
  idLocal     int(10) NOT NULL, 
  PRIMARY KEY (idHorario_A));
CREATE TABLE CANCHA (
  idCancha    int(10) NOT NULL AUTO_INCREMENT, 
  descripcion varchar(255), 
  precio      numeric(5, 2), 
  puntuacion  numeric(4, 2), 
  estado      char(1), 
  idLocal     int(10) NOT NULL, 
  idDeporte   int(10) NOT NULL, 
  PRIMARY KEY (idCancha));
CREATE TABLE DEPORTE (
  idDeporte int(10) NOT NULL AUTO_INCREMENT, 
  nombre    varchar(25), 
  estado    char(1), 
  PRIMARY KEY (idDeporte));
CREATE TABLE CARACTERISTICA (
  idCaracteristica int(10) NOT NULL AUTO_INCREMENT, 
  nombre           varchar(15), 
  estado           char(1), 
  PRIMARY KEY (idCaracteristica));
CREATE TABLE FOTO (
  idFoto   int(10) NOT NULL AUTO_INCREMENT, 
  nombre   varchar(15), 
  foto     varchar(255), 
  idCancha int(10) NOT NULL, 
  PRIMARY KEY (idFoto));
CREATE TABLE HORARIO (
  idHorario int(10) NOT NULL AUTO_INCREMENT, 
  h_inicio  timestamp NULL, 
  h_fin     timestamp NULL, 
  estado    char(1), 
  idCancha  int(10) NOT NULL, 
  PRIMARY KEY (idHorario));
CREATE TABLE RESERVA (
  idReserva  int(10) NOT NULL AUTO_INCREMENT, 
  fecha      date, 
  comentario varchar(255), 
  idPersona  int(10) NOT NULL, 
  idHorario  int(10) NOT NULL, 
  PRIMARY KEY (idReserva));
CREATE TABLE TIPO_DOC (
  idTipoDoc int(10) NOT NULL AUTO_INCREMENT, 
  nombre    varchar(9), 
  estado    char(1), 
  PRIMARY KEY (idTipoDoc));
CREATE TABLE CANCHA_CARACTERISTICA (
  idCancha         int(10) NOT NULL, 
  idCaracteristica int(10) NOT NULL, 
  puntaje          numeric(4, 2), 
  PRIMARY KEY (idCancha, 
  idCaracteristica));
ALTER TABLE USUARIO ADD CONSTRAINT FKUSUARIO875353 FOREIGN KEY (idTipoUsuario) REFERENCES TIPO_USUARIO (idTipoUsuario);
ALTER TABLE PERSONA ADD CONSTRAINT FKPERSONA271369 FOREIGN KEY (idUsuario) REFERENCES USUARIO (idUsuario);
ALTER TABLE LOCAL ADD CONSTRAINT FKLOCAL975666 FOREIGN KEY (idPersona) REFERENCES PERSONA (idPersona);
ALTER TABLE PERSONA ADD CONSTRAINT FKPERSONA861058 FOREIGN KEY (idTipoDoc) REFERENCES TIPO_DOC (idTipoDoc);
ALTER TABLE SUSCRIPCION ADD CONSTRAINT FKSUSCRIPCIO619558 FOREIGN KEY (idUsuario) REFERENCES USUARIO (idUsuario);
ALTER TABLE SUSCRIPCION ADD CONSTRAINT FKSUSCRIPCIO478794 FOREIGN KEY (idPlan) REFERENCES `PLAN` (idPlan);
ALTER TABLE COMPROBANTE ADD CONSTRAINT FKCOMPROBANT917823 FOREIGN KEY (idSuscripcion) REFERENCES SUSCRIPCION (idSuscripcion);
ALTER TABLE COMPROBANTE ADD CONSTRAINT FKCOMPROBANT732562 FOREIGN KEY (idFormaPago) REFERENCES FORMA_PAGO (idFormaPago);
ALTER TABLE CANCHA ADD CONSTRAINT FKCANCHA441147 FOREIGN KEY (idLocal) REFERENCES LOCAL (idLocal);
ALTER TABLE CANCHA ADD CONSTRAINT FKCANCHA689641 FOREIGN KEY (idDeporte) REFERENCES DEPORTE (idDeporte);
ALTER TABLE FOTO ADD CONSTRAINT FKFOTO951013 FOREIGN KEY (idCancha) REFERENCES CANCHA (idCancha);
ALTER TABLE HORARIO ADD CONSTRAINT FKHORARIO91629 FOREIGN KEY (idCancha) REFERENCES CANCHA (idCancha);
ALTER TABLE HORARIO_ATENCION ADD CONSTRAINT FKHORARIO_AT335309 FOREIGN KEY (idLocal) REFERENCES LOCAL (idLocal);
ALTER TABLE RESERVA ADD CONSTRAINT FKRESERVA543160 FOREIGN KEY (idPersona) REFERENCES PERSONA (idPersona);
ALTER TABLE RESERVA ADD CONSTRAINT FKRESERVA519950 FOREIGN KEY (idHorario) REFERENCES HORARIO (idHorario);
ALTER TABLE CANCHA_CARACTERISTICA ADD CONSTRAINT FKCANCHA_CAR756916 FOREIGN KEY (idCancha) REFERENCES CANCHA (idCancha);
ALTER TABLE CANCHA_CARACTERISTICA ADD CONSTRAINT FKCANCHA_CAR399680 FOREIGN KEY (idCaracteristica) REFERENCES CARACTERISTICA (idCaracteristica);
