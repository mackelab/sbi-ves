import {jwtDecode} from 'jwt-decode';

interface JwtObject {
  id: string;
  email: string;
  username: string;
  roles: string[];
  sub: string | null;
  exp: number;
}

/**
 * This function parses the given JSON Web Token to retrieve its payload and data.
 * It returns a JSON Object with the two keys:
 * - 'sub' containing the username
 * - 'exp' containing the expiry date as a Unix Timestamp in seconds
 *
 * @param {string}  token  The JSON Web Token
 */
export function parseJwt(token: string): JwtObject {
  return jwtDecode(token);
}

/**
 * This function parses the given JSON Web Token and checks whether it is expired
 *
 * @param {string}  token  The JSON Web Token
 * @returns {boolean} whether or not the JWT did expire
 */
export function tokenExpired(token: string): boolean {
  return Date.now() / 1000 > parseJwt(token).exp;
}

/**
 * This function parses the given JSON Web Token and returns the username string
 *
 * @param {string}  token  The JSON Web Token
 * @returns {string} the username stored in the JWT
 */
export function getUsername(token: string): string | null {
  return parseJwt(token).sub;
}
