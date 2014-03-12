#include <stdio.h>

/*
 * tool to drop inode cache -- workaround for a bug in linux 2.6.18 (debian)
 * where too many inodes are kept in cache when many files are copied -- this
 * can me made setuid executable by the group performing the roundup backup.
 */

int main ()
{
	FILE *fp = fopen ("/proc/sys/vm/drop_caches", "w");
	if (fp)
	{
		fprintf (fp, "2");
		fclose (fp);
	}
	else
	{
		return -1;
	}
	return 0;
}
