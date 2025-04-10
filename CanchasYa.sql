CREATE TABLE usuario (
  dni            int(8) NOT NULL AUTO_INCREMENT, 
  apellidos      varchar(100) NOT NULL, 
  nombres        varchar(100) NOT NULL, 
  correo         varchar(100) NOT NULL UNIQUE, 
  telefono       char(9), 
  contraseña     varchar(255) NOT NULL, 
  token          varchar(255) NOT NULL, 
  fecha_registro date, 
  estado_usuario char(1) NOT NULL comment 'A = "Activo" //pago suscripcion
I = "Inactivo" //no pago suscripcion
V = "Vetado" // algo hizo mal', 
  fotoDoc1       varchar(100), 
  fotoDoc2       varchar(100), 
  id_tipousuario int(10) NOT NULL, 
  `Column`       int(10), 
  PRIMARY KEY (dni));
CREATE TABLE tipo_usuario (
  id_tipousuario int(10) NOT NULL AUTO_INCREMENT, 
  nombre         char(2) NOT NULL comment 'A = "Administrador"
V = "Vendedor"
U = "Usuario"', 
  PRIMARY KEY (id_tipousuario));
CREATE TABLE negocio (
  id_negocio       int(10) NOT NULL AUTO_INCREMENT, 
  nombre           varchar(50) NOT NULL, 
  telefono_negocio char(9) NOT NULL, 
  ruc              char(14) NOT NULL, 
  ubicacion        varchar(255) NOT NULL, 
  enlace_ftnegocio varchar(255) NOT NULL, 
  id_usuario       int(8) NOT NULL, 
  usuarionombres   varchar(100) NOT NULL, 
  usuarionombres2  varchar(100) NOT NULL, 
  PRIMARY KEY (id_negocio));
CREATE TABLE horario_atencion (
  id_horario int(10) NOT NULL AUTO_INCREMENT, 
  turno      char(1) NOT NULL comment 'M = "Mañana"
T = "Tarde-noche"', 
  PRIMARY KEY (id_horario));
CREATE TABLE horario_atencion_negocio (
  id_horario  int(10) NOT NULL, 
  id_negocio  int(10) NOT NULL, 
  hora_inicio time(7) NOT NULL, 
  hora_fin    time(7) NOT NULL, 
  PRIMARY KEY (id_horario, 
  id_negocio));
CREATE TABLE cancha (
  id_cancha       int(10) NOT NULL AUTO_INCREMENT, 
  descripcion     varchar(255) NOT NULL, 
  precio_hora     numeric(9, 2) NOT NULL, 
  enlace_ftcancha varchar(255) NOT NULL, 
  id_negocio      int(10) NOT NULL, 
  id_tipocancha   int(10) NOT NULL, 
  PRIMARY KEY (id_cancha));
CREATE TABLE tipo_cancha (
  id_tipocancha int(10) NOT NULL AUTO_INCREMENT, 
  tipo_deporte  varchar(50) NOT NULL, 
  PRIMARY KEY (id_tipocancha));
CREATE TABLE suscripcion (
  id_suscripcion     int(10) NOT NULL AUTO_INCREMENT, 
  nombre_suscripcion varchar(50) NOT NULL, 
  precio_suscripcion numeric(9, 2) NOT NULL, 
  PRIMARY KEY (id_suscripcion));
CREATE TABLE detalle_suscripcion (
  id_detallesuscripcion int(10) NOT NULL AUTO_INCREMENT, 
  id_usuario            int(8) NOT NULL, 
  id_suscripcion        int(10) NOT NULL, 
  fecha_suscripcion     date NOT NULL, 
  fin_suscripcion       date NOT NULL, 
  fecha_pago            date NOT NULL, 
  precio_suscripcion    numeric(9, 2) NOT NULL, 
  usuarionombres        varchar(100) NOT NULL, 
  usuarionombres2       varchar(100) NOT NULL, 
  PRIMARY KEY (id_detallesuscripcion));
CREATE TABLE comprobante_pago (
  id_comprobante        int(10) NOT NULL AUTO_INCREMENT, 
  igv                   numeric(9, 2) NOT NULL, 
  precio_sinigv         numeric(9, 2) NOT NULL, 
  total                 numeric(9, 2) NOT NULL, 
  tipo_comprobante      char(1) NOT NULL comment 'F = "Factura"
B = "Boleta"', 
  id_formapago          int(10) NOT NULL, 
  id_detallesuscripcion int(10) NOT NULL, 
  PRIMARY KEY (id_comprobante));
CREATE TABLE forma_pago (
  id_formapago int(10) NOT NULL AUTO_INCREMENT, 
  nombre       varchar(50) NOT NULL comment 'Y = "Yape"
T = "Tarjeta"', 
  PRIMARY KEY (id_formapago));
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
ALTER TABLE usuario ADD CONSTRAINT FKusuario749490 FOREIGN KEY (id_tipousuario) REFERENCES tipo_usuario (id_tipousuario);
ALTER TABLE negocio ADD CONSTRAINT FKnegocio995409 FOREIGN KEY (id_usuario) REFERENCES usuario (dni);
ALTER TABLE horario_atencion_negocio ADD CONSTRAINT FKhorario_at842385 FOREIGN KEY (id_horario) REFERENCES horario_atencion (id_horario);
ALTER TABLE horario_atencion_negocio ADD CONSTRAINT FKhorario_at892204 FOREIGN KEY (id_negocio) REFERENCES negocio (id_negocio);
ALTER TABLE cancha ADD CONSTRAINT FKcancha676582 FOREIGN KEY (id_negocio) REFERENCES negocio (id_negocio);
ALTER TABLE cancha ADD CONSTRAINT FKcancha205820 FOREIGN KEY (id_tipocancha) REFERENCES tipo_cancha (id_tipocancha);
ALTER TABLE detalle_suscripcion ADD CONSTRAINT FKdetalle_su97979 FOREIGN KEY (id_usuario) REFERENCES usuario (dni);
ALTER TABLE detalle_suscripcion ADD CONSTRAINT FKdetalle_su249090 FOREIGN KEY (id_suscripcion) REFERENCES suscripcion (id_suscripcion);
ALTER TABLE comprobante_pago ADD CONSTRAINT FKcomprobant87721 FOREIGN KEY (id_detallesuscripcion) REFERENCES detalle_suscripcion (id_detallesuscripcion);
ALTER TABLE comprobante_pago ADD CONSTRAINT FKcomprobant453742 FOREIGN KEY (id_formapago) REFERENCES forma_pago (id_formapago);
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
