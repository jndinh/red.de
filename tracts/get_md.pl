use strict;
use warnings;

while (<>) {
    if ($_ =~ /.*,24.*/) {
        print "$_";
    }
}
