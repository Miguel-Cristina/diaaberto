--
-- Dumping data for table `campus`
--

INSERT INTO `campus` (`id`, `nome`, `morada`, `contacto`) VALUES
(1, 'Campus das Gambelas', 'R. dos Malmequeres 101, 8005-139 Faro', '289 800 100'),
(2, 'Campus da Penha', 'Estrada da Penha, 8000-139 Faro', '289 800 101');

-- --------------------------------------------------------

--
-- Dumping data for table `departamento`
--

INSERT INTO `departamento` (`id`, `nome`, `faculdade_id`) VALUES
(1, 'Departamento de Ciências Sociais e da Educação', NULL),
(2, 'Departamento de Comunicação, Artes e Design', NULL),
(3, 'Departamento de Línguas, Literaturas e Culturas', NULL),
(4, 'Departamento de Ciências Exatas, Naturais e Desporto', NULL),
(5, 'Departamento de Engenharia Alimentar', NULL),
(6, 'Departamento de Engenharia Civil', NULL),
(7, 'Departamento de Engenharia Eletrotécnica', NULL),
(8, 'Departamento de Engenharia Mecânica', NULL),
(9, 'Departamento de Análises Clínicas e Saúde Pública', NULL),
(10, 'Departamento de Dietética e Nutrição', NULL),
(11, 'Departamento de  Enfermagem', NULL),
(12, 'Departamento de Farmácia', NULL),
(13, 'Departamento de Ortoprotesia', NULL),
(14, 'Departamento de Radiologia', NULL),
(15, 'Departamento de Terapia da Fala', NULL),
(16, 'Departamento de Psicologia e Ciências de Educação', NULL),
(17, 'Departamento de Artes e Humanidades', NULL),
(18, 'Departamento de Ciências Biológicas e bioengenharia', NULL),
(19, 'Departamento de Ciências da Terra, do Mar e do Ambiente', NULL),
(20, 'Departamento de Engenharia Electrónica e Informática', NULL),
(21, 'Departamento de Física', NULL),
(22, 'Departamento de Matemática', NULL),
(23, 'Departamento de Química e Farmácia', NULL);

-- --------------------------------------------------------


--
-- Dumping data for table `edificio`
--

INSERT INTO `edificio` (`id`, `nome`, `campus_id`) VALUES
(1, 'Edificio 1: FCHS', 2),
(10, 'Edificio 22: ESGHT', 1),
(11, 'Edificio 23: ESEC', 1),
(14, 'Edificio 26: SAS', 1),
(12, 'Edificio 27: ISE', 1),
(13, 'Edificio 28: ISE', 1),
(15, 'Edificio 29: CP', 1),
(2, 'Edificio 2: FCT', 2),
(17, 'Edificio 30: Biblioteca', 1),
(16, 'Edificio 30: CP', 1),
(18, 'Edificio 32: ISE-Civil', 1),
(19, 'Edificio 33: Serviços Técnicos', 1),
(3, 'Edificio 3: CP', 2),
(4, 'Edificio 4: Grande Auditório', 2),
(5, 'Edificio 5: Reitoria|Biblioteca', 2),
(6, 'Edificio 6: Cantina', 2),
(7, 'Edificio 7: FCT', 2),
(8, 'Edificio 8: FCT', 2),
(9, 'Edificio 9: FE', 2),
(20, 'Pavilhões: J\'s', 2);
-- --------------------------------------------------------
--
-- Dumping data for table `utilizadortipo`
--
INSERT INTO `utilizadortipo` (`id`, `tipo`) VALUES
(1, 'Participante Individual'),
(2, 'Docente'),
(3, 'Colaborador'),
(4, 'Coordenador'),
(5, 'Administrador'),
(6, 'Participante em Grupo');
-- --------------------------------------------------------
--
-- Dumping data for table `sala`
--
INSERT INTO `sala` (`id`, `identificacao`, `edificio_id`) VALUES
(37, '0.12', 7),
(16, '0.22', 1),
(38, '0.32', 7),
(10, '1.53', 1),
(12, '1.55', 1),
(15, '1.59', 1),
(13, '1.6', 1),
(11, '1.64', 1),
(23, '1B', 9),
(1, '2.11', 3),
(17, '2.12', 8),
(2, '2.13', 3),
(9, '2.37', 2),
(7, '2.5', 3),
(21, '2A', 9),
(20, '3.24', 8),
(18, '3.42', 2),
(19, '3.44', 2),
(8, '3.5', 3),
(14, 'Anfiteatro 1.8', 8),
(22, 'Anfiteatro 1A', 9),
(24, 'Anfiteatro 3B', 9),
(3, 'Anfiteatro A', 3),
(4, 'Anfiteatro B', 3),
(5, 'Anfiteatro C', 3),
(6, 'Anfiteatro D', 3),
(33, 'J10', 20),
(34, 'J11', 20),
(35, 'J12', 20),
(25, 'J2', 20),
(26, 'J3', 20),
(27, 'J4', 20),
(28, 'J5', 20),
(29, 'J6', 20),
(30, 'J7', 20),
(31, 'J8', 20),
(32, 'J9', 20),
(36, 'Laboratório B', 9);
-- --------------------------------------------------------
--
-- Dumping data for table `tipoatividade`
--
INSERT INTO `tipoatividade` (`id`, `tipo`) VALUES
(3, 'Atividades Experimentais'),
(4, 'Atividades Tecnológicas'),
(7, 'Conferências'),
(13, 'Exposições'),
(5, 'Feira das Ciências'),
(15, 'Outras Atividades'),
(11, 'Outras Atividades (Culturais)'),
(12, 'Outras Atividades (Desportivas)'),
(10, 'Outras Atividades (Ensino)'),
(6, 'Palestras'),
(14, 'Passeios'),
(27, 'Passeios na praia'),
(8, 'Seminários'),
(9, 'Tertúlias'),
(1, 'Visitas Instalações'),
(2, 'Visitas Laboratórios');
-- --------------------------------------------------------
--
-- Dumping data for table `unidadeorganica`
--
INSERT INTO `unidadeorganica` (`id`, `nome`, `campus`) VALUES
(1, 'Escola Superior de Educação e Comunicação', 2),
(2, 'Escola Superior de Gestão, Hotelaria e Turismo', 2),
(3, 'Escola Superior de Saúde', 1),
(4, 'Escola Superior de Engenharia', 2),
(5, 'Faculdade de Ciências Humanas e Sociais', 1),
(6, 'Faculdade de Ciências e Tecnologia', 1),
(7, 'Faculdade de Economia', 2),
(8, 'Departamento de Ciências Biomédicas e Medicina', 1);
-- --------------------------------------------------------
--
-- Dumping data for table `diaaberto`
--
INSERT INTO `diaaberto` (`id`, `titulo`, `descricao`, `email`, `contacto`, `data_inicio`, `data_fim`, `limite_inscricao_atividades`, `limite_inscricao_participantes`) VALUES
(1, 'Dia Aberto Universidade do Algarve', 'Venha conhecer a Universidade do Algarve e descobrir qual a tua vocação profissional, antes de decidires qual o teu curso superior!', 'geral@ualg.pt', 289111111, '2020-02-02', '2020-03-03', 60, 880),
(2, 'Dia Aberto da Universidade do Algarve 2021', 'Evento direcionado aos alunos que procuram ingressar no ensino superior, disponibilizando atividades, workshops e palestras para te ajudar a decidir o teu futuro. Junta-te a nós e faz parte da universidade de onde é bom viver!', 'diaabaerto@ualg.pt', 289100100, '2020-02-02', '2020-02-02', 60, 800);
-- --------------------------------------------------------
--
-- Dumping data for table `ementa`
--
INSERT INTO `ementa` (`id`, `preco_aluno_normal`, `preco_outro_normal`) VALUES
(1, '2.40', '2.80');
-- --------------------------------------------------------
--
-- Dumping data for table `faculdade`
--
INSERT INTO `faculdade` (`id`, `nome`) VALUES
(1, 'Faculdade de Artes e Letras'),
(2, 'Faculdade de Ciências e Tecnologia'),
(3, 'Faculdade de Ciências Humanas e Sociais'),
(4, 'Faculdade de Economia'),
(5, 'Faculdade de Engenharia'),
(7, 'Faculdade de Medicina');
-- --------------------------------------------------------
--
-- Dumping data for table `publicoalvo`
--
INSERT INTO `publicoalvo` (`id`, `nome`) VALUES
(3, '10º ano'),
(4, '11º ano'),
(5, '12º ano'),
(1, '8º ano'),
(2, '9º ano'),
(10, 'Artes Visuais'),
(7, 'Ciências e Tecnologias'),
(8, 'Ciências Socioeconómicas'),
(11, 'Ensino Profissional'),
(9, 'Línguas e Humanidades'),
(6, 'Todos');
-- --------------------------------------------------------
--
-- Dumping data for table `sessao`
--
INSERT INTO `sessao` (`id`, `hora`) VALUES
(10, '09:00:00.000000'),
(2, '10:00:00.000000'),
(3, '11:00:00.000000'),
(4, '12:00:00.000000'),
(5, '14:00:00.000000'),
(6, '15:00:00.000000'),
(7, '16:00:00.000000'),
(8, '17:00:00.000000'),
(13, '18:00:00.000000');
-- --------------------------------------------------------
--
-- Dumping data for table `tematica`
--
INSERT INTO `tematica` (`id`, `tema`) VALUES
(1, 'Arte'),
(2, 'Biologia'),
(3, 'Ciências'),
(4, 'Desporto'),
(8, 'Economia'),
(9, 'Gestão'),
(5, 'Informática'),
(6, 'Saúde'),
(7, 'Terapêutica');
-- -------------------------------------------------------
--
-- Dumping data for table `unidadeorganica_departamento`
--
INSERT INTO `unidadeorganica_departamento` (`id`, `unidade_organica`, `departamento`) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 1, 3),
(4, 1, 4),
(5, 4, 5),
(6, 4, 6),
(7, 4, 7),
(8, 4, 8),
(9, 3, 9),
(10, 3, 10),
(11, 3, 11),
(12, 3, 12),
(13, 3, 13),
(14, 3, 14),
(15, 3, 15),
(16, 5, 16),
(17, 5, 17),
(18, 6, 18),
(19, 6, 19),
(20, 6, 20),
(21, 6, 21),
(22, 6, 22),
(23, 6, 23);
-- --------------------------------------------------------
--
-- Dumping data for table `utilizador_tarefa`
--
INSERT INTO `utilizador_tarefa` (`id`, `tarefa_id`, `coordenador_id`, `colaborador_id`, `colaboracao_id`, `estado`) VALUES
(1, 1, 1, 1, 1, NULL),
(2, 2, 1, 1, 3, NULL),
(3, 3, 1, 1, 6, NULL),
(4, 4, 1, 1, 7, NULL);
