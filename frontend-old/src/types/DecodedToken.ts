import { Usuario } from "./Usuario";

export interface DecodedToken {
    usuario: Usuario;
    // Puedes agregar más propiedades si tu token las tiene
}