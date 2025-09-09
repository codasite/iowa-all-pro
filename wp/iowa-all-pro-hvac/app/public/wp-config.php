<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the installation.
 * You don't have to use the web site, you can copy this file to "wp-config.php"
 * and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * Database settings
 * * Secret keys
 * * Database table prefix
 * * Localized language
 * * ABSPATH
 *
 * @link https://wordpress.org/support/article/editing-wp-config-php/
 *
 * @package WordPress
 */

// ** Database settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'local' );

/** Database username */
define( 'DB_USER', 'root' );

/** Database password */
define( 'DB_PASSWORD', 'root' );

/** Database hostname */
define( 'DB_HOST', 'localhost' );

/** Database charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8' );

/** The database collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );

/**#@+
 * Authentication unique keys and salts.
 *
 * Change these to different unique phrases! You can generate these using
 * the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}.
 *
 * You can change these at any point in time to invalidate all existing cookies.
 * This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY',          'Z?)G>!A:B9)mx$l:e-*GhrIjo1IVvTVu!z/bX;`hV>RH,cV?j&}Uc=;g7Jqds~0@' );
define( 'SECURE_AUTH_KEY',   '}GmSwz@u+PL7&1&Mrw@dSK]tM0TOzJOMe9g~Om_;!=]+HxRN.uV^$Rqr{|qELyVK' );
define( 'LOGGED_IN_KEY',     'SI:fcHz2wsd*CYC|6Z_b2h}.(1K9|Yiy&WsU!g6@S<`#JII^d0B~z[h8nbs47.4/' );
define( 'NONCE_KEY',         'wnWq<f ,jG09yae[2qbTBx/UbU8gxJ<+p$p9*9]Vq:!T6_Ym01u9L~PjS4S7Rz8s' );
define( 'AUTH_SALT',         '<J#bl~RIDoRXSnwQ$[E-CGczQ[!SYnV2OK1YPM-;S0&R+,]XZ[Fkx__>7Zhh]>,z' );
define( 'SECURE_AUTH_SALT',  'oyOwJh^x`lIp<3Hw=ds)Fz!bKQNA[,e4PVH%gEH[Lydu9.(l()x91E0}n<sQb@-8' );
define( 'LOGGED_IN_SALT',    'N9_Lx+|sTm/Dy^Z.}H[vu* 1I5K(BUPD[tCxH+B4LR3WTIxa-I9%Up)W,pg9|>gZ' );
define( 'NONCE_SALT',        '_9bEIJe$R2Bx[A_xu:JiH>vLA0psW^XoJD%a5QZoS%VW?MF3XN?(h&(}$_,>CpxL' );
define( 'WP_CACHE_KEY_SALT', 'qEsqPf;E8 89b_y&PweBUxX M+_-&3fXuTEJJ EiWJ)34Q0~qozHQqS|k6lF@d{r' );


/**#@-*/

/**
 * WordPress database table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = 'wp_';


/* Add any custom values between this line and the "stop editing" line. */



/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the documentation.
 *
 * @link https://wordpress.org/support/article/debugging-in-wordpress/
 */
if ( ! defined( 'WP_DEBUG' ) ) {
	define( 'WP_DEBUG', false );
}

define( 'WP_ENVIRONMENT_TYPE', 'local' );
/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', __DIR__ . '/' );
}

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';
