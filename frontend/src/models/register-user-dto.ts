/* tslint:disable */

/* eslint-disable */

/**
 * DTO representation of a User.
 * @export
 * @interface RegisterUserDto
 */
export interface RegisterUserDto {
  /**
   *
   * @type {string}
   * @memberof RegisterUserDto
   */
  'id'?: string | null;
  /**
   *
   * @type {string}
   * @memberof RegisterUserDto
   */
  'firstName': string;
  /**
   *
   * @type {string}
   * @memberof RegisterUserDto
   */
  'lastName': string;
  /**
   *
   * @type {string}
   * @memberof RegisterUserDto
   */
  'institution': string;
  /**
   * @type {string}
   * @memberof RegisterUserDto
   */
  'username': string;

  /**
   * @type {string}
   * @memberof RegisterUserDto
   */
  'email': string;

  /**
   * @type {string}
   * @memberof RegisterUserDto
   */
  'password': string;

  /**
   * @type {string}
   * @memberof RegisterUserDto
   */
  'confirmPassword': string;

}



