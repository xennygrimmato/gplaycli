import os
import hashlib
import subprocess

TESTAPK='org.mozilla.focus'
TOKENFILE=os.path.expanduser('~/.cache/gplaycli/token')

def call(args):
	return subprocess.run(args.split()).returncode

def download_apk():
	call("gplaycli -vd %s" % TESTAPK)

def checksum(apk):
	return hashlib.sha256(open(apk, 'rb').read()).hexdigest()

def test_download():
	if os.path.isfile(TOKENFILE):
		os.remove(TOKENFILE)
	download_apk()
	assert os.path.isfile("%s.apk" % TESTAPK)

def test_alter_token():
	token = open(TOKENFILE).read()
	token = ' ' + token[1:]
	with open(TOKENFILE, 'w') as outfile:
		print(token, file=outfile)
	download_apk()
	assert os.path.isfile("%s.apk" % TESTAPK)

def test_update(apk="tests/com.duckduckgo.mobile.android_3.0.17.apk"):
	before = checksum(apk)
	call("gplaycli -vyu tests")
	after = checksum(apk)
	assert after != before

def test_search(string='fire', number=30):
	ecode = call("gplaycli -s %s -n %d" % (string, number))
	assert ecode == 0

def test_search2(string='com.yogavpn'):
	ecode = call("gplaycli -s %s" % string)
	assert ecode == 0

#def test_search3(string='com.yogavpn', number=15):
#	ecode = call("gplaycli -s %s -n %d" % (string, number))
#	assert ecode == 0

def test_another_device(device='hammerhead'):
	call("gplaycli -vd %s -dc %s" % (TESTAPK, device))
	assert os.path.isfile("%s.apk" % TESTAPK)

def test_download_additional_files(apk='com.mapswithme.maps.pro'):
	call("gplaycli -d %s -a" % apk)
	assert os.path.isfile("%s.apk" % apk)
	files = [f for f in os.listdir() if os.path.isfile(f)]
	assert any([f.endswith('%s.obb' % apk) and f.startswith('main') for f in files])
	assert any([f.endswith('%s.obb' % apk) and f.startswith('patch') for f in files])
