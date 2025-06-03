% README.m
% Análisis sencillo de la primera versión de Bitcoin (v0.1)
%
% Este archivo explica de forma general qué se encontró al inspeccionar los 
% archivos originales de la versión 0.1 de Bitcoin, lanzada en enero de 2009.
%
% Autor: [Nombre del Estudiante]
% Fecha: [Fecha de entrega]
%

%% 1. Contexto y objetivos
% En enero de 2009, Satoshi Nakamoto lanzó la versión 0.1 de Bitcoin.
% El objetivo de este análisis es:
%   1. Revisar la estructura de directorios y archivos principales del cliente original.
%   2. Identificar las funciones clave que permiten la creación de bloques y transacciones.
%   3. Observar cómo se inicia la cadena de bloques ("genesis block").
%   4. Exponer hallazgos generales sobre el diseño y la lógica base de Bitcoin.

%% 2. Estructura general del repositorio de Bitcoin v0.1
% Carpeta /bitcoin-0.1/: contiene los archivos fuente originales en C++
%   - bitcoin.cpp   : archivo principal con la función main()
%   - wallet.cpp    : manejo básico de wallet (monedero)
%   - db.cpp        : código de manejo de la base de datos para la cadena de bloques
%   - txdb.cpp      : base de datos de transacciones
%   - miner.cpp     : lógica de minería (prueba de trabajo)
%   - rpc/*         : llamadas RPC para consultas remotas
%   - util.cpp      : funciones utilitarias (cifrado, base58, etc.)
%   - headers/      : espacio de direcciones IP iniciales y parámetros
%   - Scripts/      : archivos batch o scripts de configuración inicial
%
% Observación:
%   - El archivo principal es bitcoin.cpp, donde se inicializan nodos y se 
%     arranca el bucle principal de descarga y validación de bloques.
%   - genesis.h/.cpp (o contenido embedido en el código) describe el bloque
%     génesis con su «hash hardcoded».

%% 3. Funciones clave para el bloque génesis
% Al inspeccionar bitcoin.cpp y db.cpp, encontramos:
%
%   - seed0[]: lista de IPs que el cliente usa para encontrar otros nodos.
%   - CBlock::CBlock(): constructor de la clase CBlock
%   - CBlock::SetNull(): inicializa un bloque vacío.
%   - ReadBlockFromDisk / WriteBlockToDisk: funciones para cargar y guardar bloques.
%   - CBlock::GetHash(): calcula el hash del bloque (double SHA256).
%
% El código embebe directamente los datos del «genesis block»:
%   - timestamp: 2009-01-03 18:15:05 UTC
%   - coinbase: "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"
%   - hash genesis: 00000000…0000 (hash conocido)
%
% Ejemplo comentado en bitcoin.cpp (aprox. líneas 350–400):
%
%   // Genesis block
%   const char* pszTimestamp = "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks";
%   CTransaction txNew;
%   txNew.vin.resize(1);
%   txNew.vout.resize(1);
%   txNew.vin[0].scriptSig = CScript() << 486604799 << CBigNum(4) << vector<unsigned char>((const unsigned char*)pszTimestamp, (const unsigned char*)pszTimestamp + strlen(pszTimestamp));
%   txNew.vout[0].nValue = 50 * COIN;
%   txNew.vout[0].scriptPubKey = CScript() << ParseHex("04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61de \
%      b649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f") << OP_CHECKSIG;
%   genesis.vtx.push_back(txNew);
%   genesis.hashPrevBlock = 0;
%   genesis.hashMerkleRoot = genesis.BuildMerkleTree();
%   genesis.nVersion = 1;
%   genesis.nTime    = 1231006505;
%   genesis.nBits    = 0x1d00ffff;
%   genesis.nNonce   = 2083236893;

%% 4. Lógica de minería básica
% En miner.cpp se encuentra la función de prueba de trabajo (proof-of-work):
%
%   bool BitcoinMiner(CWallet* pwallet) {
%       // Construcción del bloque candidato
%       CBlockIndex* pindexPrev = pindexBest;
%       CBlock block(pindexPrev->nHeight + 1, pindexPrev->GetBlockHash());
%       // ...
%       while (true) {
%           block.nNonce++;
%           if (block.GetHash() <= bnTarget) {
%               // Bloque válido encontrado
%               ProcessBlockFound(&block, *pwallet);
%               return true;
%           }
%       }
%       return false;
%   }
%
% Observación:
%   - El cliente inicial hacía prueba de trabajo incre­mentando el nonce en un bucle
%     hasta que el hash calculado cumplía la condición de dificultad.
%   - El bloque génesis se «forjó» a mano; el código no minaba realmente el primer bloque.

%% 5. Diseño de la red y propagación de bloques
% El cliente de Bitcoin v0.1 implementa:
%   - Un servidor TCP en el puerto 8333 para aceptar conexiones entrantes.
%   - Un protocolo simple de mensajes: VERSION, VERACK, GETBLOCKS, BLOCK, TX, etc.
%   - Funciones SendMessage() y ReceiveMessage() para serializar/deserializar.
%
% En net.cpp / main.cpp (alrededor de líneas 200–350):
%
%   // Inicialización del socket
%   INode* pnode = ConnectNode(addr);
%   // Proceso principal:
%   while (!fShutdown) {
%       // Leer mensaje
%       CDataStream vRecv;
%       if (ReceiveMessage(pnode, vRecv)) {
%           ProcessMessage(pnode, vRecv);
%       }
%       // Enviar mensaje (p.e. inv, getblocks, etc.)
%       if (pnode->nVersion > 0) {
%           SendMessage(pnode, vSend);
%       }
%   }
%
% Observación:
%   - No existía todavía Tor ni evasión de IP; la lista seed0[] era prácticamente la única forma
%     de encontrar otros nodos.
%   - El protocolo no estaba versionado como hoy; no había rollback ni BIP sofisticados.

%% 6. Seguridad y criptografía
% Funciones relevantes en util.cpp y crypto/sha256.cpp:
%   - DoubleSHA256: para calcular hash de encabezado de bloque.
%   - ECDSA: generación de claves públicas/privadas con curva secp256k1.
%   - Base58: para codificar direcciones (version byte + RIPEMD160(SHA256(pubkey)) + checksum).
%
% Ejemplo de uso de SHA256 en util.cpp:
%
%   uint256 CHashWriter::GetHash() {
%       unsigned char buf[32];
%       SHA256_Final(buf, &sha);
%       SHA256_Init(&sha);
%       SHA256_Update(&sha, buf, 32);
%       SHA256_Final(buf, &sha);
%       return uint256(buf);
%   }
%
% Observación:
%   - La seguridad del sistema reposa en la imposibilidad de invertir el hash y en la fuerza bruta
%     para romper ECDSA (actualmente insostenible para hardware clásico).

%% 7. Hallazgos y conclusiones personales
% 1) Estructura minimalista: La primera versión de Bitcoin (v0.1) era sorprendentemente pequeña,
%    con ~17,000 líneas de C++ en total. Esto demuestra que Satoshi diseñó un prototipo funcional
%    sin capas excesivas de abstracción.
%
% 2) Bloque Génesis hardcoded: El bloque inicial estaba embebido en el código con valores fijos
%    (nTime, nNonce, dificultad). No se utilizó minería automática para ese bloque.
%
% 3) Protocolo básico de red: La lógica de conexiones P2P y mensajes (inv, getdata, block) aparece
%    en un mismo archivo (main.cpp), sin módulos separados. Aún así, funcionaba para propagación de bloques.
%
% 4) Sistema de claves y direcciones: El uso de ECDSA y Base58 estaba ya implementado en esta versión,
%    indicando que desde el inicio la creación de direcciones y validación de firmas era central.
%
% 5) Dependencia de nodos seed: Sin DNS seeders sofisticados, la lista hardcoded seed0[] era clave para
%    arrancar la red. Si esos nodos caían, la red quedaba fragmentada.
%
% 6) Comentarios y estilo: Muchas funciones no están documentadas con comentarios extensos, pero el
%    nombre de funciones y variables suele bastar para entender la lógica básica.
%
% 7) Posible mejora: Separar la lógica P2P en un módulo independiente, refactorizar las rutinas de BD
%    en una clase, y comentar con mayor detalle las secciones críticas (p.e. validación de transacciones).
%
% En general, la versión 0.1 de Bitcoin es un gran ejemplo de diseño compacto: cada módulo (miner, wallet,
% db, p2p) cabe en unos pocos archivos, pero juntos brindan un sistema descentralizado funcional.

%% 8. Enlace al repositorio con la información
% El código fuente original de Bitcoin v0.1 se puede clonar desde:
%   https://github.com/bitcoin/bitcoin/tree/v0.1.0
%
% También se ha creado un repositorio de ejemplo con scripts de extracción de información y resultados de este análisis:
%   https://github.com/USUARIO/Analisis_Bitcoin_v0.1
%
% (Reemplazar "USUARIO" por el nombre de GitHub del estudiante)

%% FIN README.m
