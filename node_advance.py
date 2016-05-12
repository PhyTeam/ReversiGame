import gmpy2

from node import Node

# Declare const
C_PLAYER1, C_PLAYER2 = 1, -1
shift_left_mask = -9187201950435737472
shift_right_mask = 72340172838076673

inv_slm = ~shift_left_mask
inv_srm = ~shift_right_mask

# Types and constants used in the functions below

m1 = 0x5555555555555555  # binary: 0101...
m2 = 0x3333333333333333  # binary: 00110011..
m4 = 0x0f0f0f0f0f0f0f0f  # binary:  4 zeros,  4 ones ...
m8 = 0x00ff00ff00ff00ff  # binary:  8 zeros,  8 ones ...
m16 = 0x0000ffff0000ffff  # binary: 16 zeros, 16 ones ...
m32 = 0x00000000ffffffff  # binary: 32 zeros, 32 ones
hff = 0xffffffffffffffff  # binary: all ones
h01 = 0x0101010101010101  # the sum of 256 to the power of 0,1,2,3...

index64 = [
    0, 47, 1, 56, 48, 27, 2, 60,
    57, 49, 41, 37, 28, 16, 3, 61,
    54, 58, 35, 52, 50, 42, 21, 44,
    38, 32, 29, 23, 17, 11, 4, 62,
    46, 55, 26, 59, 40, 36, 15, 53,
    34, 51, 20, 43, 31, 22, 10, 45,
    25, 39, 14, 33, 19, 30, 9, 24,
    13, 18, 8, 12, 7, 6, 5, 63
]

# Highly random numbers - use for hash
random_number_A = [
    0x86245617, 0x503A9AF9, 0xF0422F2C, 0x8C16FF64, 0x42A38A72, 0x6B0B821E, 0x5597279A, 0xC3754059,
    0x95847DFF, 0x6E43C58A, 0xE79D6F04, 0xED723A97, 0xFFAFFD19, 0x4AFD7444, 0xA57220B8, 0x2B0D6830,
    0xA8433F7C, 0xCBEE30C5, 0x3C4F008F, 0xE47C1D1D, 0x88EAA9A3, 0xB813A88E, 0x7314732A, 0x705C9A78,
    0x882D1CAA, 0xD8E223DC, 0xEF76542B, 0x7A69AA1D, 0xB8E64C81, 0x40A4E35E, 0xF37FF97F, 0x49A3F06D,
    0x58A869F3, 0x682E85BD, 0x346607C7, 0xBA406F56, 0x968F0992, 0x50C81F72, 0x582D3D6C, 0x4C3A6D42,
    0x7B27F2E9, 0x3F2F300A, 0x0182FDDB, 0x8B132F2A, 0xCAEA985A, 0x2D5A007C, 0xD8A7A3B1, 0xD8B0F67B,
    0x50946E8A, 0xEBE4E3C6, 0xF9F9ED21, 0xD7BF810A, 0xE43103B8, 0x2BAAD119, 0xB87C60A2, 0x90BB3711,
    0xC8AF18D2, 0x5A4E2EA9, 0x70A01E1A, 0x78AE807D, 0x1AF8CEFE, 0x1CBA24EF, 0x9CD376D6, 0xF8D2D980,

    0x682C01A3, 0xAE5D997B, 0x3E82C8C5, 0xBE1EAA20, 0x2EC45F0E, 0x7A10649E, 0x3A82A77D, 0x3C50A11C,
    0x042D575C, 0x594D18BE, 0x7DDFF125, 0x1F916BEB, 0xAA0676FB, 0x049AD118, 0xB93B9971, 0x40D80142,
    0xCF1D7AB4, 0x725D3A03, 0xCEE29AB3, 0x4D1D7FB2, 0x425813F9, 0x66E9C302, 0x3402F871, 0xF779DD08,
    0xD834D17A, 0xD9EBF420, 0xF9A8B1D6, 0x27652E58, 0xDA04E9B6, 0x092A7AE6, 0xC253EDA7, 0x95F03DA8,
    0x86F616FC, 0xE23599E3, 0xACEC2191, 0x8C02F63B, 0xEF4B2A30, 0xDEB5061D, 0xDE14A304, 0x58ECFEA9,
    0xE9E78059, 0x3A0B95AB, 0xF2DEFA77, 0x1661986A, 0x26A669F0, 0xDFB4BE3E, 0x6480B82B, 0xA176A95C,
    0xBC4F11B7, 0x578CECFA, 0x107B2F53, 0xC8DADC94, 0xC2E953BC, 0x96BC408D, 0x549F02BF, 0xAB1461D3,
    0xD8C381C2, 0xA6FAA77C, 0x55B789C0, 0xB4702389, 0xB915A6B9, 0xA7ADC7D2, 0xDB88549E, 0x6A3AB129,

    0xB278806D, 0x30AF7D43, 0xBF9E4C8F, 0x3057F6C1, 0x19720CB5, 0x400189AF, 0x73AF4EF6, 0x9B358518,
    0x660B5AA7, 0x24ADE7C8, 0xFE50D619, 0x9BF049E7, 0x13D9EA82, 0xA9F5C838, 0x23F40F52, 0x84E97AEF,
    0xDB02661F, 0x910357FA, 0xBD150E60, 0x24DD2949, 0x06AC4EFD, 0xC5232C5B, 0xA75A364E, 0x5DF06043,
    0x53D0EC57, 0xD03D1124, 0xC2CD958D, 0x344C6C13, 0x3D4C646C, 0xC4DE9FD6, 0xC7FB4173, 0x5E8CC28D,
    0xCB646CAD, 0x9F7450B6, 0xDBC37C60, 0x1985080D, 0x7F114F2A, 0x213A981C, 0x631D2244, 0x86268B22,
    0xBD65E530, 0xAC8BF541, 0x7E25BCBE, 0x3877CA02, 0x102A9B97, 0xFED4D3D2, 0x7FB9AFDB, 0xC1895E25,
    0xA917F46B, 0xDE7C020A, 0xC0E7223B, 0x53157C82, 0x243976F9, 0xD6964BC6, 0xFEE7DB68, 0x64F32811,
    0x26AA7952, 0x6E6739E3, 0x1CF09317, 0x3475DEDC, 0x3017E9A7, 0xFABD4752, 0x7EDB6387, 0x081A1600,

    0x9A185D70, 0x53D34651, 0x39326F28, 0x115A461E, 0xB8E6AD43, 0xCC92170E, 0x1CE419CD, 0xFE7CA536,
    0x188678D5, 0x7D80B2E3, 0x0711946D, 0x1977BED8, 0x7333BFE1, 0x4DFE00F6, 0xC71FD5BB, 0x8DC0CD9A,
    0xB249B685, 0xDD53693F, 0x39081613, 0x7C63C821, 0xA033F991, 0x2AB40C5E, 0xAAE60F56, 0x58AFC9D1,
    0x820A721C, 0xF98E39CB, 0xD6E4AEEE, 0x79673DA2, 0xA1BBFF80, 0x1CBE0C5A, 0xC13D8412, 0x9615510D,
    0x612F82D3, 0x783534A6, 0x7DF99F46, 0x652E20DF, 0x5C51AA1C, 0x273BEE79, 0xA462A470, 0x8035D542,
    0x15F4AAC2, 0xD06130C2, 0x9FCB5B1C, 0xCC124BA3, 0x4C1264A8, 0x7D1FA7A8, 0xD0BF63A0, 0x49F69518,
    0x2F2918CD, 0xD78CEB04, 0x749C056E, 0x333EEFF0, 0x8CFC4680, 0x50033B44, 0x9E40FD2A, 0xEC9442CF,
    0x94E461C9, 0x0AC18751, 0x9CF79980, 0xC7F5046D, 0x76594132, 0x050B10FD, 0x390DEC91, 0x6DF7E480
]

random_number_B = [
    0x7CC3DDE0, 0x2B03292D, 0x8B55B0ED, 0xE82A5C24, 0xED498B2B, 0xE11DCF5D, 0x3DDD421D, 0x4729FF7C,
    0xE4E8A02B, 0x7779DE28, 0xCC9DBC23, 0x0EED2A5E, 0x5DB0541D, 0x6369323C, 0x2B00C6B7, 0x20A2CE2C,
    0x59F86473, 0x1F4D5FA7, 0xB26BA74A, 0xFB23BBDA, 0x48832471, 0xA3F5612B, 0xDABC8F8C, 0xE3B6E6C5,
    0x257479A1, 0xB1AEFD88, 0x964E0DDD, 0xD90E5A70, 0x2579E10B, 0x578D2EFD, 0xF971325A, 0x07F7966B,
    0xE8175225, 0x0A7B595B, 0xF0519E4E, 0x52D49A64, 0x3DF980F8, 0x569163DC, 0x06BDA18E, 0x7824AA48,
    0xA7F12980, 0x8842E652, 0x44E6A04B, 0x21C24524, 0x32D1E4D8, 0x0DF97EEC, 0x4AEFAB8D, 0x7E955EDA,
    0xC646AD35, 0x11F3A69F, 0x9081A025, 0x3443DEFA, 0x8A014A5D, 0x993801DB, 0x431252A1, 0xEE2FC7EA,
    0xB2CC58F8, 0x02553A18, 0x1FD33B9F, 0x20D190CE, 0x0EFC9C90, 0xDE5FC4F1, 0x408E81B4, 0x245D3C55,

    0x6F967E19, 0x39238F10, 0xBE22BA63, 0x81F5F967, 0xB424EC1B, 0x27651856, 0x93FD1AA4, 0x1C2D04CD,
    0xF54C462E, 0xB2476EA2, 0xF522FBC9, 0xA280140A, 0x1BBACA6A, 0x73629950, 0x821D6BE6, 0x7EA6BF4B,
    0xF3440966, 0x598F8E89, 0x8E07DB29, 0xFC90AD68, 0x8DAFEEB6, 0x2906BEFC, 0xB0994D9B, 0xD851191E,
    0xB26EE762, 0x03BC4F0F, 0x547930E6, 0x0B0E5352, 0x0ABFE8AE, 0x3E54AD6D, 0x475E0DE6, 0x755A53D6,
    0x7B11607F, 0x3DD1CFE3, 0xA279A00B, 0x93847074, 0x226E0C64, 0x48EF854A, 0x60B2C498, 0xA07CE774,
    0x987D5B2C, 0xC05A1E1E, 0x3848A370, 0x2ED6F9CC, 0xEBFAFF4E, 0x52C94EF9, 0xA15C805E, 0x06FF8A0F,
    0xC3A6B6F4, 0x2AF1EF5E, 0xF88CF0DD, 0x7B9E5729, 0x97A1A106, 0x4C79BE56, 0xC6146EAA, 0x1D7B199F,
    0x7195E31C, 0x5122E5F3, 0x29DC5510, 0xB183494B, 0x4F4FE658, 0xA79F4F6A, 0x4B4B15D5, 0x06DEAABA,

    0xD72E9AD4, 0x4D624FBB, 0x08B6E69E, 0x8B70C42D, 0x7EEA5252, 0x4B6920D2, 0x58D31455, 0xFF20FAA1,
    0xA325D4AA, 0x56773A4E, 0xBE43C241, 0xF54C7D0E, 0x809475DD, 0xCAEE54D5, 0x49205C1C, 0xA5E7175E,
    0xD5AEED1E, 0xB2A5C408, 0x5E54E15E, 0x7A3F351E, 0xD983F9EC, 0xE203D316, 0xF8A66932, 0xB0BE9A4A,
    0x4E9F01AE, 0xA38E1EE7, 0x28968E6F, 0x91275CD9, 0x827FABBB, 0xFDD663D0, 0xDC3468EA, 0xDA1FDA00,
    0xFFFBF240, 0xE1BDDBBF, 0x57D99133, 0x3C59082F, 0x55BC9348, 0x18546C78, 0x55D4A420, 0xED68A70D,
    0x26CE52D6, 0x1573FD4F, 0xE8128AAB, 0xE870A668, 0x907A1908, 0x4472D61C, 0xF819C0A2, 0x73A2CF24,
    0x57CB9D2B, 0x43AD3190, 0x708A3C54, 0x7A5EA724, 0xB3F52836, 0x4E73A2E3, 0x1AA0361F, 0x63424CB8,
    0xA1895E87, 0x339F11DA, 0xDDF4F294, 0x9A88CDAB, 0x68A43D92, 0x31F3ADE2, 0xB99C241E, 0x0F5B86D6,

    0x46ABA56E, 0xCAEEF1D4, 0x096B027D, 0xCF4FA759, 0x6C675FAF, 0x7120760D, 0xA1F9A82F, 0xAB70B90D,
    0xDDD715E3, 0xE55B2462, 0x4F6564CA, 0x1E31CFC0, 0xCFB6C5D7, 0xA3BC6F41, 0x8414A9A4, 0xEA71633D,
    0x923A634F, 0x39367C5C, 0x9B4FD8C5, 0x07E8084B, 0x5EC6C791, 0x3DA0D7EE, 0x3B463CEC, 0x3AFDB9E9,
    0xD25F9AFD, 0x957CADF2, 0xEB5EC331, 0xACD624F4, 0xB547E4ED, 0x82A6A0F3, 0x3EE2C795, 0x498D2820,
    0x11D7A07E, 0x36F7493B, 0xF49B33E0, 0x943C14DF, 0x932555F9, 0xD506600F, 0xBD5AF924, 0xEC388D72,
    0xBCE7AEB0, 0x0A929DAA, 0x37FBE49B, 0xCEA2083C, 0x28BA97AA, 0xE79D4146, 0x575BF4BA, 0xD2F024E5,
    0xDADA4BD1, 0x6023ADB7, 0x6582994E, 0x48D5E0B2, 0x69F33F43, 0x64CD78C8, 0x3944C6AF, 0x08399E94,
    0x036A5014, 0xAAD9C7DE, 0xF6F1168B, 0x9D0FBB5E, 0x5B2F60AD, 0x74D18806, 0xD01E59EB, 0xE7B9258F
]

random_number_C = [
    0x2A258760, 0x9A6C6A67, 0xECABEAAD, 0xFCA96F7E, 0xD96BF1F9, 0x9C8E339E, 0x9B5310F5, 0x7528CFF7,
    0x543592C6, 0xD1191F3C, 0xD4C436C9, 0xDDD48EEE, 0x88C239CD, 0x71C5C63C, 0x835311EB, 0x77EA390A,
    0x2507897F, 0x2B121694, 0x26B125C7, 0x9215530E, 0xE6136812, 0xEAE8D127, 0x2C5AD1FE, 0xFC4C08A3,
    0xFF73845F, 0x912F2378, 0x502F28C2, 0x4D97D420, 0x041F345C, 0xF7423CA6, 0x538A74AD, 0x3BF81D32,
    0xE6540EF5, 0x148ADD8D, 0xE5F7F618, 0x608470EA, 0x2D5EF795, 0x56BEF4DB, 0x4CEE8A6E, 0xB5F1FE89,
    0x28310F6F, 0xB5269BBC, 0x09519C3D, 0x444C7D18, 0x8B60E059, 0xFD3502E3, 0x75E0ACB6, 0x09C707C2,
    0xC096E576, 0x02CE9A5D, 0xC6EF4E2A, 0x79473074, 0x1AB48343, 0x685D1634, 0xAE96523A, 0x4E69518C,
    0x6A0FD7FA, 0xE8E457D0, 0x91620945, 0x6E8B8AA8, 0x1383EF74, 0xAAE087BA, 0x41A1B622, 0xFF99C8B3,

    0xC9D0D08E, 0x23E6861E, 0x568771B2, 0xF3DF52FF, 0x765C76FD, 0x89778844, 0x01778641, 0xDA5B3278,
    0xF60C86E8, 0xB947EC7B, 0x4B0239F8, 0xAA076062, 0x598FA4B0, 0x7FB2F100, 0x6FC32D8E, 0x85EF4B3D,
    0x6E181B42, 0x31875DFA, 0xFCF65B83, 0x93202FEE, 0xB4504AD0, 0xB5671649, 0x8C7C5B78, 0xEDA41797,
    0x177A616A, 0x9EB1B30B, 0x9D1EBFB9, 0x1DB0DDC5, 0x522429A5, 0x811728C7, 0x83A6CC36, 0x4B92B521,
    0x734282AD, 0xF683D179, 0xB868F9A5, 0x90DD045D, 0xEFD23DC6, 0xBE080A61, 0x37B3B644, 0xE94E383E,
    0x3E5C25B0, 0xC7FBEF78, 0x58B82F9E, 0x85E9E99B, 0x328911E2, 0x9B754F4B, 0xBFE7A25A, 0xC193829E,
    0x408A22B7, 0x193ABE7B, 0x7F76FD1C, 0xB9BDB60B, 0x86CDA3B3, 0x0D73B665, 0xEFE4EAB2, 0xC9E24C30,
    0x65B27A28, 0xBA75933C, 0xC307FD26, 0x04D8E006, 0xE3A8C168, 0x4CA0171B, 0xFEC4A356, 0x828C0414,

    0x5C21103B, 0x5CB12592, 0x62536805, 0x65E1DDB1, 0xD7C7116F, 0x713B73D4, 0x5D8AA571, 0x7A38A532,
    0x9E91CE4D, 0xDBF89308, 0xE5258959, 0xE2E54E15, 0xD85B7B5F, 0x8CDAF7AE, 0xFFB5F57B, 0x679F89C9,
    0xF9953C67, 0x2AE6DBEC, 0xFE4F0C46, 0x572804FF, 0x591D65B1, 0x2A548BB7, 0xD37195BB, 0x7C457092,
    0x35D891DA, 0xAC1B21D9, 0x6FC2B231, 0xC72A56AF, 0xFD4A03E5, 0xC87A20D8, 0x05F33172, 0x3874E2ED,
    0x1C9F7881, 0xC2A6D7FB, 0xD61B74C7, 0x401A9544, 0x13F6ADFE, 0xFED682BD, 0xD59FE240, 0x03FB58D9,
    0x52B6B492, 0x53B3FF93, 0x75BE5FBC, 0x53993866, 0x27CF0111, 0x0E043BDE, 0xFCDB8FE1, 0x898AB564,
    0xBA3314C9, 0x7A24DFED, 0x642E9B1C, 0x2F11CAC2, 0x575DF356, 0xA04EA642, 0x3418BA79, 0xA304057D,
    0x1865CAE1, 0x89EF85F4, 0x89B995AB, 0x5BE751C4, 0xF5B85FD8, 0x91ACF488, 0x8F84CD79, 0x9ECDC690,

    0xE1B9B1AE, 0x656B7524, 0xB959F493, 0x09F474F0, 0x785506A4, 0x236EBF48, 0xF10FF08E, 0x2476AEFD,
    0x54B554CC, 0x2F2B3BEB, 0x73289531, 0x9884ACD6, 0xF68932E8, 0x8EBB6002, 0xDA620FBB, 0x246B2530,
    0x38FA4AFB, 0xCC670452, 0xBB8224FD, 0x430A173A, 0xC59F5423, 0x3A3A121C, 0x27A7E861, 0x3142A023,
    0x326F8C2D, 0x696700E5, 0x036585E3, 0x533C8107, 0x02135E1F, 0xF2BC42ED, 0x18DCABD2, 0xA00AF343,
    0xAB45D251, 0x9D80B62B, 0x8B554601, 0x0233006A, 0xF2BFEBE2, 0x1B6BFE72, 0xA4AA8845, 0x674F928E,
    0x4BE46A25, 0x476DA5D4, 0x4FB33F64, 0x23C11EBF, 0x3ABE06CF, 0x3B3F5061, 0x547B8CAA, 0x43DD34B2,
    0x2D42240E, 0xDF1ABB20, 0x5C0D3C28, 0xA7B72448, 0xC1EFEBFB, 0x4BD259C7, 0xBCFCBB1F, 0x1DF3411C,
    0x313AC0FD, 0x8318D9A1, 0x32751B51, 0x299893E2, 0x386D2422, 0x04DB7222, 0x0042E73F, 0xA0A29322,
]

random_number_D = [
    0xAB6CDFAF, 0x02C32214, 0x75897C35, 0xF6BB670C, 0xE7FD801A, 0x341E6DFE, 0xCD006F2F, 0xD3536EBC,
    0x0DD716E3, 0x5503C9A6, 0x7287BD50, 0x3CC25368, 0x922A1664, 0x75AFC1C8, 0x76E07D8B, 0x38CD904E,
    0xC85B8503, 0x2DF21972, 0xDDB86F8C, 0xE86C88D1, 0xB152AD85, 0xBC57C233, 0x049859FD, 0xDF732DE9,
    0x801D8C41, 0x7E6BDD4E, 0x40FB302F, 0xD6F15627, 0xC4FB977C, 0x60B5A3A8, 0x19428B22, 0xA739E904,
    0xE2CC8B97, 0x6A0EF477, 0x1EB0B85B, 0x1355E522, 0xA9309C51, 0x2C3D626A, 0x9A83B2C2, 0xDE9E9379,
    0x64D3AFBE, 0xDE1236A8, 0xC67AB431, 0xA1133451, 0x2BCA36C7, 0xB22F6B4A, 0x77B923DA, 0x034C0202,
    0x85FE8029, 0x29D7E621, 0xD1DD67BE, 0x920CB8F9, 0xA0BB8092, 0xACB09BD6, 0x982F3701, 0xDFF0A5D9,
    0x2F634F7E, 0x8E4139C1, 0x4125F66C, 0xEEF56946, 0x206E63E0, 0x66B19AAC, 0x27551312, 0x7CFDAEE7,

    0x7EED5D7B, 0xC68E60B1, 0xE814B44C, 0x60EB3980, 0x8B2D5A6F, 0xCDFA8A64, 0x872E01C2, 0xAB755B59,
    0xF9E4632E, 0x1C8E1859, 0xB3331E11, 0x4C09CF75, 0xFC94DBB6, 0xCEFC1FEE, 0xAB58842B, 0xDACED6CB,
    0xBB881967, 0xDC9EB464, 0xF9B86F7B, 0xEECDDE8A, 0x0552FAB3, 0xA38E558E, 0x4221AE55, 0x4BD86665,
    0x90EFAEE9, 0x6CCD3FD6, 0x5A352D44, 0x9AD56A19, 0xE42A7BFE, 0x832BDBEF, 0xBA4C27C4, 0x05CB1B1B,
    0xA20512DC, 0x8B95B54D, 0x900FA7EE, 0x7D0F0DC7, 0x11AA81AE, 0xB307A5AF, 0x65C0DB05, 0x508B2322,
    0x6F1A41CB, 0x3A176737, 0x74CDAB8A, 0x6CC88DFA, 0x761003BB, 0xA6FA7205, 0xE836096E, 0x8B59B7CE,
    0xD27646A5, 0x17807F12, 0x908A52E3, 0x0E0CE7DB, 0xBC854A9D, 0xAFE56B01, 0xC33ADCCD, 0x87B6C392,
    0x2EBEB664, 0x63264999, 0x53C5FE35, 0xF784C7D4, 0x8A900591, 0xA12C108A, 0x6D5D6159, 0xD149CA12,

    0x512663A8, 0xEB35A2C6, 0x3834487F, 0x69B3F51B, 0xF7EAFD6F, 0x6E411A21, 0x16C70951, 0x9943060A,
    0xA607CF62, 0x38C67A55, 0x594CE03E, 0xD2A23CEE, 0x01DD254E, 0x2110A216, 0x38974A43, 0x7ED3322D,
    0xF3741A73, 0x06E757FA, 0x627E8055, 0x4F93A8A3, 0x9E4844C8, 0xBF9AA887, 0x5B812D84, 0x1EEE6255,
    0xD6672E05, 0xBCD705A5, 0x75C306FE, 0xB5385C08, 0xD47F749D, 0x4CE5A555, 0xBE8AAA63, 0xA7413A1F,
    0xF76CFB70, 0x5182FEA7, 0x73A2F52A, 0x198FC14A, 0x03EC4224, 0x22C62EBE, 0x29F7B616, 0xD68BB1ED,
    0x2918A88C, 0x26E7CDBB, 0x058B4167, 0x8C8521D6, 0x67885980, 0x8AA412C7, 0x61C35887, 0x4D6E9664,
    0x023E8964, 0x4BD189A4, 0xEB146CEE, 0x5A9A44A6, 0x7F772522, 0x139A502B, 0x3CD43237, 0x3CAB8D7F,
    0xAB4F19FF, 0x26861FF0, 0x4C922681, 0xA774A9FA, 0x072D5591, 0x35394885, 0xB1C83DF2, 0x118582B1,

    0x4D4E28DD, 0x329439F3, 0xF8C1E3B3, 0x3CA88997, 0x319260B2, 0xA6C5035B, 0x87915B73, 0x89CA9A79,
    0x28E88810, 0x957CEA22, 0x56BD5E71, 0xDCFE2B8A, 0xFA3DAE06, 0xB950A03B, 0x9AE05D75, 0x2E97041E,
    0x9CC3324B, 0xAA225834, 0x59860348, 0xD112D8A8, 0x7EEF4C07, 0xD1B50C88, 0x50D5866B, 0xE04C1FC2,
    0xBDD0652D, 0xC10A56B5, 0xF2D47930, 0x9E9D66A9, 0x6BBCD62D, 0x9267FC88, 0x42C1EFA1, 0x57AA6B4F,
    0x432E982E, 0x62BDFB7D, 0x60A0A581, 0xC2368C76, 0xE87EB7D9, 0x95F3CF6A, 0xB5EF5137, 0x139705D7,
    0x0256D928, 0x8010E7CB, 0x40B56705, 0x25205C31, 0x37CAE89F, 0xFE474D86, 0x2DA18898, 0x54FD2E71,
    0x3EBCB4B1, 0x46C7D034, 0xE3EE3A11, 0x6DC56495, 0x9213D223, 0xD5B519D1, 0x76CC3ED5, 0x85E391E6,
    0xE8612ADC, 0x722FA377, 0x7D21B4FD, 0xCAC74A2F, 0xFFA04368, 0xA33A6E97, 0xE10278AC, 0xB107F5AE
]

def bitScanForward(bb):
    """
    Using de Bruijn Sequences to Index a 1 in a Computer Word
    :param bb: bb bitboard to scan
    :precondition bb != 0
    :return: index (0..63) of least significant one bit
    """
    debruijn64 = 0x03f79d71b4cb0a89
    return index64[((bb ^ (bb - 1)) * debruijn64) >> 58]

def popcount(x):
    """
    Efficient methods for counting the on-bits in an integer
    It uses 17 arithmetic operations.
    """
    # x -= (x >> 1) & m1  # put count of each 2 bits into those 2 bits
    # x = (x & m2) + ((x >> 2) & m2)  # put count of each 4 bits into those 4 bits
    # x = (x + (x >> 4)) & m4  # put count of each 8 bits into those 8 bits
    # x += x >> 8  # put count of each 16 bits into their lowest 8 bits
    # x += x >> 16  # put count of each 32 bits into their lowest 8 bits
    # x += x >> 32  # put count of each 64 bits into their lowest 8 bits
    # return x & 0x7f
    # Using library
    return gmpy2.popcount(x)

def shift_left(position):
    return (position >> 1) & inv_slm


def shift_right(position):
    return (position << 1) & inv_srm


def shift_down(position):
    return position >> 8


def shift_up(position):
    return position << 8


def shift_left_up(position):
    return ((position >> 1) & inv_slm) << 8


def shift_left_down(position):
    return ((position >> 1) & inv_slm) >> 8


def shift_right_up(position):
    return ((position << 1) & inv_srm) << 8


def shift_right_down(position):
    return ((position << 1) & inv_srm) >> 8


direction = {
    'UPP': shift_up,
    'DOW': shift_down,
    'LEF': shift_left,
    'RIG': shift_right,
    'LUP': shift_left_up,
    'LDO': shift_left_down,
    'RUP': shift_right_up,
    'RDO': shift_right_down
}

inv_direction = {
    'UPP': shift_down,
    'DOW': shift_up,
    'LEF': shift_right,
    'RIG': shift_left,
    'LUP': shift_right_down,
    'LDO': shift_right_up,
    'RUP': shift_left_down,
    'RDO': shift_left_up
}


def dilation(bits, d=None, is_inverted=False):
    if d is not None:
        if is_inverted:
            return inv_direction[d](bits)
        else:
            return direction[d](bits)
    else:
        return bits | shift_up(bits) | shift_down(bits) | \
               shift_left(bits) | shift_right(bits) | \
               shift_left_down(bits) | shift_left_up(bits) | \
               shift_right_up(bits) | shift_right_down(bits)


class BitBoard(Node):

    bitboard = {
        # 0x00\00\00\08\10\00\00\00
        C_PLAYER1: 0x0000000810000000,
        C_PLAYER2: 0x0000001008000000
    }

    def __position(self, row, col):
        return 1 << (row * 8 + col)

    def __set_at(self, pos, player):
        self.bitboard[player] = (self.bitboard[player] & ~pos) | pos

    def __get_at(self, pos, player):
        return self.bitboard[player] & pos

    def one_bits(self, bits):
        """
        Calculate index of 1s bit in bitstring
        :param bits: bb
        :return: List index of
        """
        if bits == 0:
            return []
        else:
            bb = bits
            result = []
            while bb != 0:
                index = bitScanForward(bb)
                result.append(index)
                bb &= ~(1 << index)
            return result


    def __to_x_y(self, board):

        to_x_y = []
        for i in xrange(0, 64, 8):
            temp = board >> i & 0xFF
            if temp != 0:
                for j in xrange(8):
                    valid = temp & 1
                    temp >>= 1
                    if valid != 0:
                        to_x_y.append((i / 8, j))
        return to_x_y

    def __generate_flipped_squares(self, move, dir, player):
        flipped_bit = move
        is_end = 0xFFFFFFFFFFFFFFFF
        while is_end != 0:
            move = dilation(move, dir, True)
            is_end = move & self.bitboard[player]
            flipped_bit |= move
        return flipped_bit

    def __gererate_new_board(self, flipped_squares, player):
        new_board = {C_PLAYER1: self.bitboard[C_PLAYER1], C_PLAYER2: self.bitboard[C_PLAYER2]}

        # Add to player bitboard
        new_board[player] |= flipped_squares
        # Clear opponent
        new_board[-player] &= ~flipped_squares
        return new_board

    def __str__(self):
        tostring = ""
        for i in xrange(8):
            for j in xrange(8):
                pos = self.__position(i, j)
                if self.__get_at(pos, C_PLAYER1) != 0:
                    tostring += '1'
                elif self.__get_at(pos, C_PLAYER2) != 0:
                    tostring += '2'
                else:
                    tostring += '0'
            tostring += '\n'
        return tostring

    def __init__(self, board):
        super(BitBoard, self).__init__(board)
        self._hashcode = 0

    def __valid_moves(self, player):
        moves = {}
        empty = ~(self.bitboard[C_PLAYER1] | self.bitboard[C_PLAYER2])
        for d in direction.keys():
            dmove = 0
            candidates = self.bitboard[-player] & dilation(self.bitboard[player], d)
            while candidates != 0:
                dmove |= empty & dilation(candidates, d)
                candidates = self.bitboard[-player] & dilation(candidates, d)
            moves[d] = dmove
        return moves

    def get_all_valid_moves(self, player):
        avalible_move = 0
        moves = self.__valid_moves(player)

        for m in moves.values():
            avalible_move |= m

        all_candidate_moves = {}
        idx = gmpy2.bit_scan1(avalible_move, 0)
        while idx is not None:
            mask = 1 << idx
            flipped_square = 0
            for dir in direction.keys():
                if mask & moves[dir] != 0:
                    flipped_square |= self.__generate_flipped_squares(mask, dir, player)
            bstr = self.__gererate_new_board(flipped_square, player)
            new_board = BitBoard(None)
            new_board.bitboard = bstr
            all_candidate_moves[(idx / 8, idx % 8)] = new_board
            idx = gmpy2.bit_scan1(avalible_move, idx + 1)

        return all_candidate_moves

    def get_mobility(self, player):
        valid_moves = self.__valid_moves(player)
        move_in_all_dir = 0
        for vm in valid_moves.values():
            move_in_all_dir |= vm
        return gmpy2.popcount(move_in_all_dir)

    def __hash__(self):
        if self._hashcode == 0:
            blo = self.bitboard[C_PLAYER1]
            bhi = (blo % 0x100000000) >> 32
            wlo = self.bitboard[C_PLAYER2]
            whi = (wlo % 0x100000000) >> 32
            self._hashcode = random_number_A[wlo & 0xFF] ^ random_number_B[((wlo % 0x100000000) >> 8) & 0xFF] ^ \
                             random_number_C[(wlo >> 16) & 0xFF] ^ random_number_D[((wlo % 0x100000000) >> 24) & 0xFF] ^ \
                             random_number_C[~whi & 0xFF] ^ random_number_A[((~whi % 0x100000000) >> 8) & 0xFF] ^ \
                             random_number_D[(~whi >> 16) & 0xFF] ^ random_number_D[((~whi % 0x100000000) >> 24) & 0xFF] ^ \
                             random_number_C[blo & 0xFF] ^ random_number_A[((blo % 0x100000000) >> 8) & 0xFF] ^ \
                             random_number_B[(blo >> 16) & 0xFF] ^ random_number_D[((blo % 0x100000000) >> 24) & 0xFF] ^ \
                             random_number_D[~bhi & 0xFF] ^ random_number_B[((~bhi % 0x100000000) >> 8) & 0xFF] ^ \
                             random_number_A[(~bhi >> 16) & 0xFF] ^ random_number_B[((~whi % 0x100000000) >> 24) & 0xFF]

        return self._hashcode

    def __eq__(self, other):
        return other.bitboard[1] == self.bitboard[1] and other.bitboard[-1] == self.bitboard[-1]

    def get_at(self, row, colunm):
        """
        This is a method to get a square in bit board
        Please note that this is LOW PERFORMANCE method
        """
        pos = self.__position(row, colunm)
        p1, p2 = self.__get_at(pos, C_PLAYER1), self.__get_at(pos, C_PLAYER2)
        if p1 == 0 and p2 == 0:
            return 0
        elif p1 != 0:
            return C_PLAYER1
        else:
            return C_PLAYER2

    def get_score(self, player):
        """ Return score if a player """
        return popcount(self.bitboard[player])




def bitboard_tostring(bits):
    seq = '\n'
    tostring = seq.join(["{0:08b}".format(bits >> (i * 8) & 0xFF) for i in range(8)])
    return tostring


save_board = []

from multiprocessing import *
def anlysis(node, depth, player):
    print depth
    if depth <= 0:
        #save_board.append(node)
        return

    lst = node.get_all_valid_moves(player)
    p = Pool(len(lst))

    def f(x):
        anlysis(x, depth - 1, -player)
        return 0

    p.map(f, lst.values())
    # for k, v in lst.iteritems():
    #    # print k
    #    anlysis(v, depth - 1, -player)


if __name__ == "__main__":
    print "Unit test for bitboard"
    bb = BitBoard(None)
    # bb.bitboard[C_PLAYER1] = 0x44
    # bb.bitboard[C_PLAYER2] = 0x28
    test = bb.get_all_valid_moves(1)
    print test
    print bb.get_mobility(1)
    for v, b in test.iteritems():
        print v
        print b
        print "\n"
    # print bb
"""
    nb = Node.create()
    start_time = 0
    for i in xrange(9,12):
        start_time = time()
        if i <= 7:
            anlysis(nb, i, 1)
        end_time = time()
        estimate1 = end_time - start_time
        start_time = time()
        anlysis(bb, i, 1)
        end_time = time()
        estimate2 = end_time - start_time
        print 'Depth = ', i, '\t', estimate1, '---------------------\t', estimate2
    if bb.bitboard[1] == bb.bitboard[1] and \
                    bb.bitboard[-1] == bb.bitboard[-1]:
        print 'OK'

"""

"""
    anlysis(bb, 6, 1)

    dup = 0
    check = {}
    for i in xrange(len(save_board)):
        c = 0
        for j in xrange(i+1, len(save_board)):
            if save_board[i].bitboard[1] == save_board[j].bitboard[1] and \
                save_board[i].bitboard[-1] == save_board[j].bitboard[-1] and not check.has_key(j):
                check[j] = 1
                dup +=1
"""
