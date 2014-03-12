# define PAM_SM_PASSWORD

# include <security/pam_modules.h>
# ifndef LINUX_PAM
# include <security/pam_appl.h>
# endif /* LINUX_PAM */
# include <syslog.h>
# include <sys/types.h>
# include <sys/socket.h>
# include <netinet/in.h>
# include <netdb.h>
# include <errno.h>

#include <stdio.h>

PAM_EXTERN int pam_sm_chauthtok
    (pam_handle_t *pamh, int flags, int argc, const char **argv)
{
    FILE *fp;
    const char         *uname;
    const char         *endptr;
    int                 i;
    long                lport;
    in_port_t           port;
    int                 sock;
    struct sockaddr_in  sin;
    struct hostent     *hp;
    
    if (argc != 2)
    {
        syslog (LOG_ERR, "pwch_notify: number of args, expected host port");
        return PAM_TRY_AGAIN;
    }
    lport = strtol (argv [1], &endptr, 10);
    if (*argv [1] == '\0' || *endptr != '\0' || lport > 0xFFFFl)
    {
        syslog (LOG_ERR, "pwch_notify: error in args, invalid port");
        return PAM_TRY_AGAIN;
    }
    port = htons ((in_port_t) lport);
    if (!(flags & PAM_UPDATE_AUTHTOK))
    {
        return PAM_SUCCESS;
    }
    if (pam_get_user (pamh, &uname, NULL) != PAM_SUCCESS || uname == NULL)
    {
        syslog (LOG_ERR, "pwch_notify: cannot get username");
        return PAM_AUTHTOK_ERR;
    }
    syslog (LOG_DEBUG, "pwch_notify: Name: %s", uname);
    if (NULL == (hp = gethostbyname (argv [0])))
    {
        syslog (LOG_ERR, "pwch_notify: unknown host: %s", argv [0]);
        return PAM_AUTHTOK_ERR;
    }
    bzero ((char *)&sin, sizeof (sin));
    bcopy(hp->h_addr, (char *)&sin.sin_addr, hp->h_length);
    sin.sin_family = hp->h_addrtype;
    sin.sin_port   = port;
    if ((sock = socket (PF_INET, SOCK_STREAM, 0)) < 0)
    {
        syslog (LOG_ERR, "pwch_notify: socket: %s", strerror (errno));
        return PAM_AUTHTOK_ERR;
    }
    if (connect (sock, (const struct sockaddr *)&sin, sizeof (sin)) < 0)
    {
        syslog (LOG_ERR, "pwch_notify: connect: %s", strerror (errno));
        return PAM_AUTHTOK_ERR;
    }
    if (NULL == (fp = fdopen (sock, "w+")))
    {
        syslog (LOG_ERR, "pwch_notify: fdopen: %s", strerror (errno));
        return PAM_AUTHTOK_ERR;
    }
    (void) fprintf (fp, "%s\n", uname);
    (void) fflush  (fp);
    if (ferror (fp))
    {
        syslog (LOG_ERR, "pwch_notify: error writing to socket");
        return PAM_AUTHTOK_ERR;
    }
    (void) fclose (fp);
    syslog (LOG_DEBUG, "pwch_notify: end", strerror (errno));
    return PAM_SUCCESS;
}
