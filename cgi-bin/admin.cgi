#!/usr/bin/perl -w

use strict;
use utf8;
use warnings;

use CGI::Session;
use Data::Dumper;
use Template;
use XML::LibXML;
use LWP::UserAgent;
use CGI;


my $parser = XML::LibXML->new();
my $doc = $parser->parse_file('../data/admins.xml');


my $cgi = CGI->new();
my $session = CGI::Session->load();

my $username;

if ($session->param('user') ne undef) {
	$username = $session->param('user');
} else {	
	$username = "admin";#$cgi->param('username');
	my $pwd = 'pwd';#$cgi->param('pwd');

	my $admin = $doc->findnodes("//admin[username='" . $username . "']");

	if (!$admin) {
		print $cgi->redirect('login.cgi?e=usr');
	} else {
		my $password = $admin->pop()->findvalue("./password");
		
		if ($password ne $pwd) {
			print $cgi->redirect('login.cgi?e=pwd');
		}

		# User exists, initialize session
		my $session = CGI::Session->new();
		$session->param('user', $username);
		print $session->header(-location=>"admin.cgi");
	} 
}


print $cgi->header( -type => "text/html", charset => 'utf-8', -status => "200 OK" );
print $cgi->start_html;

my $template = Template->new();
my $template_file = 'templates/admin.tt';

$template->process($template_file, { username => $username }) || die "Template process failed: ", $template->error(), "\n";

print $cgi->end_html;