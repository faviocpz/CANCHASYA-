DROP DATABASE IF EXISTS CanchasYa;
CREATE DATABASE CanchasYa;
USE CanchasYa;
CREATE TABLE TIPO_USUARIO (
  idTipoUsuario int(10) NOT NULL AUTO_INCREMENT, 
  tipo          char(3) NOT NULL, 
  PRIMARY KEY (idTipoUsuario));
CREATE TABLE `PLAN` (
  idPlan int(10) NOT NULL AUTO_INCREMENT, 
  nombre varchar(25) NOT NULL, 
  tarifa numeric(5, 2) NOT NULL, 
  PRIMARY KEY (idPlan));
CREATE TABLE SUSCRIPCION (
  idSuscripcion int(10) NOT NULL AUTO_INCREMENT, 
  fecha_ini     date NOT NULL, 
  fecha_fin     date NOT NULL, 
  estado        char(1) NOT NULL, 
  idPlan        int(10) NOT NULL, 
  idUsuario     int(11) NOT NULL, 
  PRIMARY KEY (idSuscripcion));
CREATE TABLE COMPROBANTE (
  numComprobante int(10) NOT NULL AUTO_INCREMENT, 
  igv            numeric(5, 2) NOT NULL, 
  subtotal       numeric(5, 2) NOT NULL, 
  total          numeric(5, 2) NOT NULL, 
  fecha          date NOT NULL, 
  idSuscripcion  int(10) NOT NULL, 
  idFormaPago    int(10) NOT NULL, 
  PRIMARY KEY (numComprobante));
CREATE TABLE FORMA_PAGO (
  idFormaPago int(10) NOT NULL AUTO_INCREMENT, 
  nombre      varchar(25) NOT NULL, 
  estado      char(1) NOT NULL, 
  PRIMARY KEY (idFormaPago));
CREATE TABLE LOCAL (
  idLocal    int(10) NOT NULL AUTO_INCREMENT, 
  nombre     varchar(50) NOT NULL, 
  direccion  varchar(60) NOT NULL, 
  tel        varchar(9) NOT NULL, 
  correo     varchar(30) NOT NULL, 
  facebook   varchar(30), 
  instagram  varchar(30), 
  puntuacion numeric(4, 2) NOT NULL, 
  estado     char(1) NOT NULL, 
  idUsuario  int(11) NOT NULL, 
  PRIMARY KEY (idLocal));
CREATE TABLE HORARIO_ATENCION (
  idHorario_A int(10) NOT NULL AUTO_INCREMENT, 
  h_inicio    timestamp NOT NULL, 
  h_fin       timestamp NOT NULL, 
  turno       varchar(15) NOT NULL, 
  estado      char(1) NOT NULL, 
  idLocal     int(10) NOT NULL, 
  PRIMARY KEY (idHorario_A));
CREATE TABLE CANCHA (
  idCancha    int(10) NOT NULL AUTO_INCREMENT, 
  descripcion varchar(255) NOT NULL, 
  precio      numeric(5, 2) NOT NULL, 
  puntuacion  numeric(4, 2) NOT NULL, 
  estado      char(1) NOT NULL, 
  idLocal     int(10) NOT NULL, 
  idDeporte   int(10) NOT NULL, 
  PRIMARY KEY (idCancha));
CREATE TABLE DEPORTE (
  idDeporte int(10) NOT NULL AUTO_INCREMENT, 
  nombre    varchar(25) NOT NULL, 
  estado    char(1) NOT NULL, 
  PRIMARY KEY (idDeporte));
CREATE TABLE CARACTERISTICA (
  idCaracteristica int(10) NOT NULL AUTO_INCREMENT, 
  nombre           varchar(15) NOT NULL, 
  estado           char(1) NOT NULL, 
  PRIMARY KEY (idCaracteristica));
CREATE TABLE FOTO (
  idFoto   int(10) NOT NULL AUTO_INCREMENT, 
  nombre   varchar(15) NOT NULL, 
  foto     varchar(255) NOT NULL, 
  idCancha int(10) NOT NULL, 
  PRIMARY KEY (idFoto));
CREATE TABLE HORARIO (
  idHorario int(10) NOT NULL AUTO_INCREMENT, 
  h_inicio  timestamp NOT NULL, 
  h_fin     timestamp NOT NULL, 
  estado    char(1) NOT NULL, 
  idCancha  int(10) NOT NULL, 
  PRIMARY KEY (idHorario));
CREATE TABLE RESERVA (
  idReserva  int(10) NOT NULL AUTO_INCREMENT, 
  fecha      date NOT NULL, 
  comentario varchar(255) NOT NULL, 
  idHorario  int(10) NOT NULL, 
  idUsuario  int(11) NOT NULL, 
  PRIMARY KEY (idReserva));
CREATE TABLE CANCHA_CARACTERISTICA (
  idCancha         int(10) NOT NULL, 
  idCaracteristica int(10) NOT NULL, 
  puntaje          numeric(4, 2) NOT NULL, 
  PRIMARY KEY (idCancha, 
  idCaracteristica));
CREATE TABLE USUARIO (
  id                  int(11) NOT NULL AUTO_INCREMENT, 
  apellidos           varchar(50) NOT NULL, 
  nombres             varchar(50) NOT NULL, 
  dni                 varchar(8) NOT NULL, 
  correo              varchar(30) NOT NULL UNIQUE, 
  telefono            varchar(9) NOT NULL, 
  foto_verificacion   varchar(250) NOT NULL, 
  contraseña          varchar(30) NOT NULL, 
  token               varchar(255) NOT NULL, 
  estado_cuenta       char(1) NOT NULL, 
  verificacion_cuenta char(1) NOT NULL CHECK (verificacion_cuenta IN ('E', 'V', 'N')), 
  idTipoUsuario       int(10) NOT NULL, 
  PRIMARY KEY (id));
ALTER TABLE USUARIO ADD CONSTRAINT FKUSUARIO875353 FOREIGN KEY (idTipoUsuario) REFERENCES TIPO_USUARIO (idTipoUsuario);
ALTER TABLE LOCAL ADD CONSTRAINT FKLOCAL226276 FOREIGN KEY (idUsuario) REFERENCES USUARIO (id);
ALTER TABLE SUSCRIPCION ADD CONSTRAINT FKSUSCRIPCIO478794 FOREIGN KEY (idPlan) REFERENCES `PLAN` (idPlan);
ALTER TABLE COMPROBANTE ADD CONSTRAINT FKCOMPROBANT917823 FOREIGN KEY (idSuscripcion) REFERENCES SUSCRIPCION (idSuscripcion);
ALTER TABLE COMPROBANTE ADD CONSTRAINT FKCOMPROBANT732562 FOREIGN KEY (idFormaPago) REFERENCES FORMA_PAGO (idFormaPago);
ALTER TABLE CANCHA ADD CONSTRAINT FKCANCHA441147 FOREIGN KEY (idLocal) REFERENCES LOCAL (idLocal);
ALTER TABLE CANCHA ADD CONSTRAINT FKCANCHA689641 FOREIGN KEY (idDeporte) REFERENCES DEPORTE (idDeporte);
ALTER TABLE FOTO ADD CONSTRAINT FKFOTO951013 FOREIGN KEY (idCancha) REFERENCES CANCHA (idCancha);
ALTER TABLE HORARIO ADD CONSTRAINT FKHORARIO91629 FOREIGN KEY (idCancha) REFERENCES CANCHA (idCancha);
ALTER TABLE HORARIO_ATENCION ADD CONSTRAINT FKHORARIO_AT335309 FOREIGN KEY (idLocal) REFERENCES LOCAL (idLocal);
ALTER TABLE RESERVA ADD CONSTRAINT FKRESERVA226487 FOREIGN KEY (idUsuario) REFERENCES USUARIO (id);
ALTER TABLE RESERVA ADD CONSTRAINT FKRESERVA519950 FOREIGN KEY (idHorario) REFERENCES HORARIO (idHorario);
ALTER TABLE CANCHA_CARACTERISTICA ADD CONSTRAINT FKCANCHA_CAR756916 FOREIGN KEY (idCancha) REFERENCES CANCHA (idCancha);
ALTER TABLE CANCHA_CARACTERISTICA ADD CONSTRAINT FKCANCHA_CAR399680 FOREIGN KEY (idCaracteristica) REFERENCES CARACTERISTICA (idCaracteristica);
ALTER TABLE SUSCRIPCION ADD CONSTRAINT FKSUSCRIPCIO640417 FOREIGN KEY (idUsuario) REFERENCES USUARIO (id);
