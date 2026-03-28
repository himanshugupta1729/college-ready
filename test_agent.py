#!/usr/bin/env python3
"""
Automated Test Agent — tests the entire flow for every grade/track combination.

Tests: registration → diagnostic → mindset quiz → archetype → report → dashboard → practice
Checks: crashes, branding, content leaks, gatekeeping, navigation

Usage:
    python3 test_agent.py                          # test against localhost:5050
    python3 test_agent.py --url https://college-ready.onrender.com  # test production
    python3 test_agent.py --track sat              # test single track
    python3 test_agent.py --ms-only                # test only middle school
    python3 test_agent.py --hs-only                # test only high school
"""

import os, sys, json, time, random, string, argparse, re
import requests
from datetime import datetime

# ── Config ──
HS_TRACKS = ['sat', 'ap_precalc', 'ap_calc_ab', 'ap_calc_bc', 'ap_stats',
             'algebra_1', 'geometry', 'algebra_2', 'precalculus', 'statistics']
MS_TRACKS = ['grade_6', 'grade_7', 'grade_7_accelerated', 'grade_8']

HS_GRADES = {
    'sat': 11, 'ap_precalc': 11, 'ap_calc_ab': 12, 'ap_calc_bc': 12,
    'ap_stats': 12, 'algebra_1': 9, 'geometry': 10, 'algebra_2': 10,
    'precalculus': 11, 'statistics': 11,
}
MS_GRADES = {
    'grade_6': 6, 'grade_7': 7, 'grade_7_accelerated': 7, 'grade_8': 8,
}

HS_EVENT = 'DEMO-2026'
MS_EVENT = 'FOUNDATION-DEMO'

VALID_ARCHETYPES = ['sigma', 'delta', 'pi', 'theta', 'phi', 'lambda', 'alpha', 'gamma']
HS_ARCHETYPE_NAMES = ['The Perfectionist', 'The Relentless', 'The Purist', 'The Quiet Genius',
                      'The Natural', 'The Dormant Force', 'The Inventor', 'The Maverick']
MS_ARCHETYPE_NAMES = ['The Machine', 'The Relentless', 'The Deep Thinker', 'The Quiet Genius',
                      'The Natural', 'The Undercover', 'The Builder', 'The Wildcard']

# Branding that should NOT appear for MS
MS_FORBIDDEN = ['SAT', 'AP Calculus', 'AP Statistics', 'AP Precalculus', 'College Ready',
                'college ready', 'SAT Math', 'AP exam', '1500']
# Branding that should NOT appear for HS
HS_FORBIDDEN = ['Foundation Math', 'Grade 6', 'Grade 7', 'Grade 8']


class TestResult:
    def __init__(self, track, step, passed, message='', details=''):
        self.track = track
        self.step = step
        self.passed = passed
        self.message = message
        self.details = details

    def __str__(self):
        icon = '✓' if self.passed else '✗'
        s = f'  {icon} [{self.track}] {self.step}: {self.message}'
        if self.details:
            s += f'\n      → {self.details}'
        return s


class TestAgent:
    def __init__(self, base_url='http://localhost:5050'):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.results = []
        self.current_track = None
        self.student_id = None

    def _url(self, path):
        return f'{self.base_url}{path}'

    def _get(self, path, **kwargs):
        return self.session.get(self._url(path), allow_redirects=True, timeout=30, **kwargs)

    def _post(self, path, data=None, **kwargs):
        return self.session.post(self._url(path), data=data, allow_redirects=True, timeout=30, **kwargs)

    def _pass(self, step, msg, details=''):
        self.results.append(TestResult(self.current_track, step, True, msg, details))

    def _fail(self, step, msg, details=''):
        self.results.append(TestResult(self.current_track, step, False, msg, details))

    def _check_branding(self, html, step, is_ms):
        """Check for branding leaks."""
        forbidden = MS_FORBIDDEN if is_ms else HS_FORBIDDEN
        found = []
        for term in forbidden:
            # Skip terms inside HTML attributes, script tags, or meta tags
            # Simple check: look in visible text areas
            if term in html:
                # Verify it's not just in a URL, attribute, or comment
                # Do a rough check - find occurrences not inside tags
                pattern = r'>[^<]*' + re.escape(term) + r'[^<]*<'
                if re.search(pattern, html):
                    found.append(term)
        if found:
            self._fail(step, f'Branding leak: found forbidden terms', ', '.join(found))
        else:
            self._pass(step, 'Branding OK — no forbidden terms found')

    def _check_no_none(self, html, step):
        """Check for None/undefined rendering errors."""
        problems = []
        if '>None<' in html or '>None ' in html:
            problems.append('None rendered in HTML')
        # Only flag 'undefined' as visible rendered text — exclude JS code in <script> tags
        html_no_scripts = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        if re.search(r'>\s*undefined\s*<', html_no_scripts):
            problems.append('undefined rendered in HTML')
        if 'Internal Server Error' in html:
            problems.append('Internal Server Error')
        if 'Traceback' in html:
            problems.append('Python traceback in HTML')
        if problems:
            self._fail(step, 'Rendering errors', ', '.join(problems))
        else:
            self._pass(step, 'No rendering errors')

    def test_registration(self, track, grade, event_code):
        """Register a test student."""
        rand = ''.join(random.choices(string.ascii_lowercase, k=4))
        email = f'test-{track}-{rand}@test.com'
        name = f'Test {track.replace("_", " ").title()}'

        data = {
            'student_name': name,
            'student_email': email,
            'parent_email': f'parent-{rand}@test.com',
            'grade': str(grade),
            'track': track,
        }

        resp = self._post(f'/register/{event_code}', data=data)

        if resp.status_code == 200:
            if 'registered' in resp.text.lower() or 'already registered' in resp.text.lower() or 'success' in resp.text.lower():
                self._pass('Registration', f'Registered {name} (grade {grade}, {track})')
                return email
            elif 'required' in resp.text.lower() or 'fill in' in resp.text.lower():
                self._fail('Registration', 'Missing required fields', f'URL: {resp.url}')
                return None
            else:
                # Registration page re-rendered — likely success
                self._pass('Registration', f'Registration submitted for {name}')
                return email
        else:
            self._fail('Registration', f'HTTP {resp.status_code}')
            return None

    def test_login(self, email, event_code):
        """Login as the test student."""
        resp = self._post('/login', data={'email': email, 'event_code': event_code})
        if resp.status_code == 200:
            if 'test' in resp.url or 'dashboard' in resp.url or 'reveal' in resp.url:
                self._pass('Login', 'Logged in successfully')
                return True
            elif 'waiting' in resp.text.lower() or 'not started' in resp.text.lower():
                self._fail('Login', 'Test not enabled for this event')
                return False
            else:
                self._pass('Login', f'Login OK, redirected to {resp.url}')
                return True
        self._fail('Login', f'HTTP {resp.status_code}')
        return False

    def test_diagnostic(self, is_ms):
        """Take the diagnostic test — answer all questions."""
        # The test flow might use different URL patterns — try several
        resp = self._get('/test')
        if resp.status_code != 200 and resp.status_code != 302:
            # Try alternate paths
            resp = self._get('/test/intro')
        if resp.status_code != 200:
            # Maybe redirected to dashboard if already done
            if 'dashboard' in resp.url or 'reveal' in resp.url or 'mindset' in resp.url:
                self._pass('Test Intro', 'Already completed, skipping')
                return True
            self._fail('Test Intro', f'HTTP {resp.status_code}, URL: {resp.url}')
            return False

        self._check_no_none(resp.text, 'Test Intro')
        self._check_branding(resp.text, 'Test Intro Branding', is_ms)

        # Start the test — find the start form/link
        # Try POST to start, or follow any start link
        resp = self._post('/test/start')
        if resp.status_code not in (200, 302):
            resp = self._get('/test/start')

        # Answer questions in a loop
        questions_answered = 0
        max_questions = 60  # safety limit

        while questions_answered < max_questions:
            # Try to get current question
            resp = self._get('/test/question')
            if resp.status_code != 200:
                # Try alternate URL
                resp = self._get('/test')

            if resp.status_code != 200:
                break

            # Check if redirected past the test
            if any(x in resp.url for x in ['mindset', 'reveal', 'dashboard', 'login']):
                break

            html = resp.text

            # Extract question ID
            q_match = re.search(r'name="question_id"\s+value="(\d+)"', html)
            if not q_match:
                q_match = re.search(r'name="qid"\s+value="(\d+)"', html)
            if not q_match:
                q_match = re.search(r'data-question-id="(\d+)"', html)
            if not q_match:
                # No question found — test might be complete
                break

            qid = q_match.group(1)
            answer = random.choice(['A', 'B', 'C', 'D'])

            # Find the submit URL
            action_match = re.search(r'action="([^"]*)"', html)
            submit_url = action_match.group(1) if action_match else '/test/answer'

            resp = self._post(submit_url, data={
                'question_id': qid,
                'answer': answer,
            })
            questions_answered += 1

        if questions_answered > 0:
            self._pass('Diagnostic', f'Answered {questions_answered} questions')
        else:
            self._fail('Diagnostic', 'No questions answered — check test flow URLs')

        return questions_answered > 0

    def test_mindset_quiz(self, is_ms):
        """Complete the mindset quiz."""
        resp = self._get('/test/mindset')
        if resp.status_code != 200:
            if 'reveal' in resp.url or 'dashboard' in resp.url:
                self._pass('Mindset Quiz', 'Already completed, redirected')
                return True
            self._fail('Mindset Quiz', f'HTTP {resp.status_code}')
            return False

        self._check_no_none(resp.text, 'Mindset Quiz Page')

        # Check MS-specific text replacement
        if is_ms and 'after high school' in resp.text:
            self._fail('Mindset Quiz Branding', '"after high school" not replaced for MS')
        elif is_ms:
            self._pass('Mindset Quiz Branding', '"after high school" correctly replaced')

        # Answer all GRIC questions
        import re
        q_names = set(re.findall(r'name="(q_\w+)"', resp.text))
        answers = {}
        for qn in q_names:
            answers[qn] = str(random.randint(1, 4))

        resp = self._post('/test/mindset', data=answers)
        if resp.status_code == 200:
            if 'reveal' in resp.url or 'archetype' in resp.url.lower():
                self._pass('Mindset Quiz', f'Completed {len(q_names)} questions, redirected to reveal')
                return True
            self._pass('Mindset Quiz', f'Submitted {len(q_names)} answers')
            return True
        self._fail('Mindset Quiz', f'HTTP {resp.status_code}')
        return False

    def test_archetype_reveal(self, is_ms):
        """Check the archetype reveal page."""
        resp = self._get('/reveal')
        if resp.status_code != 200:
            self._fail('Archetype Reveal', f'HTTP {resp.status_code}')
            return False

        html = resp.text
        self._check_no_none(html, 'Archetype Reveal')
        self._check_branding(html, 'Archetype Reveal Branding', is_ms)

        # Check archetype name appears
        names = MS_ARCHETYPE_NAMES if is_ms else HS_ARCHETYPE_NAMES
        found_name = False
        for name in names:
            if name in html:
                found_name = True
                self._pass('Archetype Name', f'Found: {name}')
                break
        if not found_name:
            self._fail('Archetype Name', 'No valid archetype name found in page')

        # Check Cuemath logo is an image, not text
        if 'cuemath-logo.svg' in html:
            self._pass('Logo', 'Cuemath logo is SVG image')
        elif '>cuemath<' in html.lower():
            self._fail('Logo', 'Cuemath logo is text, should be image')

        # Check CTAs
        if 'See Your Archetype' in html:
            self._pass('CTA', '"See Your Archetype" CTA present')
        if 'See Your Full Report' in html:
            self._pass('CTA', '"See Your Full Report" CTA present')

        return True

    def test_share_card(self):
        """Check the share card renders."""
        # Need student ID from session — try to find it
        resp = self._get('/dashboard')
        import re
        sid_match = re.search(r'/share/(\d+)', resp.text)
        if not sid_match:
            sid_match = re.search(r'/report/(\d+)', resp.text)
        if sid_match:
            self.student_id = sid_match.group(1)
            resp = self._get(f'/share/{self.student_id}')
            if resp.status_code == 200:
                self._check_no_none(resp.text, 'Share Card')
                if 'Save Image' in resp.text and 'Share' in resp.text:
                    self._pass('Share Card', 'Save Image + Share buttons present')
                else:
                    self._fail('Share Card', 'Missing Save/Share buttons')
                return True
            self._fail('Share Card', f'HTTP {resp.status_code}')
        else:
            self._fail('Share Card', 'Could not find student ID for share card')
        return False

    def test_student_report(self, is_ms):
        """Check the student report."""
        if not self.student_id:
            self._fail('Student Report', 'No student ID')
            return False

        resp = self._get(f'/report/{self.student_id}')
        if resp.status_code != 200:
            self._fail('Student Report', f'HTTP {resp.status_code}')
            return False

        html = resp.text
        self._check_no_none(html, 'Student Report')
        self._check_branding(html, 'Student Report Branding', is_ms)

        # Check FUAR scores are present
        fuar_count = 0
        for dim in ['Fluency', 'Understanding', 'Application', 'Reasoning']:
            if dim in html:
                fuar_count += 1
        if fuar_count == 4:
            self._pass('Report FUAR', 'All 4 FUAR dimensions present')
        else:
            self._fail('Report FUAR', f'Only {fuar_count}/4 FUAR dimensions found')

        return True

    def test_parent_report(self, is_ms):
        """Check the parent report."""
        if not self.student_id:
            self._fail('Parent Report', 'No student ID')
            return False

        resp = self._get(f'/report/{self.student_id}/parent')
        if resp.status_code != 200:
            self._fail('Parent Report', f'HTTP {resp.status_code}')
            return False

        html = resp.text
        self._check_no_none(html, 'Parent Report')
        self._check_branding(html, 'Parent Report Branding', is_ms)
        return True

    def test_dashboard(self, is_ms):
        """Check the dashboard."""
        resp = self._get('/dashboard')
        if resp.status_code != 200:
            self._fail('Dashboard', f'HTTP {resp.status_code}')
            return False

        html = resp.text
        self._check_no_none(html, 'Dashboard')
        self._check_branding(html, 'Dashboard Branding', is_ms)

        # Check quick links
        if '/report/' in html:
            self._pass('Dashboard Links', 'My Report link present')
        else:
            self._fail('Dashboard Links', 'My Report link missing')

        if '/reveal' in html:
            self._pass('Dashboard Links', 'My Archetype link present')
        else:
            self._fail('Dashboard Links', 'My Archetype link missing')

        if '/practice' in html:
            self._pass('Dashboard Links', 'Practice link present')
        else:
            self._fail('Dashboard Links', 'Practice link missing')

        # Check correct proficiency label
        if is_ms:
            if 'Grade-Level Proficiency' in html:
                self._pass('Dashboard Label', 'Shows "Grade-Level Proficiency" for MS')
            elif 'SAT' in html:
                self._fail('Dashboard Label', 'Shows SAT label for MS student')
        return True

    def test_practice(self):
        """Test the practice flow."""
        resp = self._get('/practice/today')
        if resp.status_code != 200:
            if 'dashboard' in resp.url:
                self._pass('Practice', 'Redirected to dashboard (plan may not be ready)')
                return True
            self._fail('Practice', f'HTTP {resp.status_code}')
            return False

        html = resp.text
        self._check_no_none(html, 'Practice')

        # Try to answer and submit
        import re
        q_names = set(re.findall(r'name="(q_\d+)"', html))
        workout_match = re.search(r'name="workout_id"\s+value="(\d+)"', html)

        if q_names and workout_match:
            answers = {'workout_id': workout_match.group(1)}
            for qn in q_names:
                answers[qn] = random.choice(['A', 'B', 'C', 'D'])

            resp = self._post('/practice/submit', data=answers)
            if resp.status_code == 200 and 'results' in resp.url:
                self._pass('Practice Submit', f'Submitted {len(q_names)} answers, got results')

                # Check results page
                html = resp.text
                self._check_no_none(html, 'Practice Results')
                if 'Step-by-Step' in html or 'steps-toggle' in html:
                    self._pass('Worked Solutions', 'Step-by-step toggle present')
                else:
                    self._fail('Worked Solutions', 'No step-by-step content found')
                return True
            else:
                self._fail('Practice Submit', f'Unexpected result: {resp.url}')
        else:
            self._pass('Practice', f'Practice page loaded ({len(q_names)} questions found)')
        return True

    def test_gatekeeping(self, is_ms):
        """Test access controls."""
        # Try accessing report without completing test (use a new session)
        fresh = requests.Session()
        resp = fresh.get(self._url('/dashboard'), allow_redirects=True, timeout=10)
        if 'login' in resp.url:
            self._pass('Gatekeeping', 'Dashboard requires login')
        else:
            self._fail('Gatekeeping', 'Dashboard accessible without login')

        resp = fresh.get(self._url('/practice/today'), allow_redirects=True, timeout=10)
        if 'login' in resp.url:
            self._pass('Gatekeeping', 'Practice requires login')
        else:
            self._fail('Gatekeeping', 'Practice accessible without login')

    def run_full_flow(self, track, grade, event_code, is_ms):
        """Run the complete test flow for one track."""
        self.current_track = track
        self.student_id = None
        self.session = requests.Session()  # fresh session

        print(f'\n{"="*60}')
        print(f'Testing: {track} (Grade {grade}, {"MS" if is_ms else "HS"})')
        print(f'{"="*60}')

        email = self.test_registration(track, grade, event_code)
        if not email:
            return

        if not self.test_login(email, event_code):
            return

        if not self.test_diagnostic(is_ms):
            return

        self.test_mindset_quiz(is_ms)
        self.test_archetype_reveal(is_ms)
        self.test_share_card()
        self.test_student_report(is_ms)
        self.test_parent_report(is_ms)
        self.test_dashboard(is_ms)
        self.test_practice()
        self.test_gatekeeping(is_ms)

    def print_summary(self):
        """Print test summary."""
        print(f'\n{"="*60}')
        print('TEST SUMMARY')
        print(f'{"="*60}')

        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = sum(1 for r in self.results if not r.passed)

        # Group by track
        tracks = {}
        for r in self.results:
            if r.track not in tracks:
                tracks[r.track] = {'pass': 0, 'fail': 0, 'failures': []}
            if r.passed:
                tracks[r.track]['pass'] += 1
            else:
                tracks[r.track]['fail'] += 1
                tracks[r.track]['failures'].append(r)

        for track, data in tracks.items():
            status = '✓ PASS' if data['fail'] == 0 else '✗ FAIL'
            print(f'\n{status} {track}: {data["pass"]} passed, {data["fail"]} failed')
            for f in data['failures']:
                print(f'    ✗ {f.step}: {f.message}')
                if f.details:
                    print(f'      → {f.details}')

        print(f'\n{"─"*60}')
        print(f'Total: {passed}/{total} passed ({failed} failed)')
        if failed == 0:
            print('🎉 All tests passed!')
        else:
            print(f'⚠️  {failed} tests need attention')

        # Save results to file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = f'test_report_{timestamp}.json'
        report = {
            'timestamp': datetime.now().isoformat(),
            'base_url': self.base_url,
            'total': total, 'passed': passed, 'failed': failed,
            'results': [{'track': r.track, 'step': r.step, 'passed': r.passed,
                         'message': r.message, 'details': r.details} for r in self.results]
        }
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        print(f'\nFull report saved to: {report_path}')


def main():
    parser = argparse.ArgumentParser(description='Test the full student flow')
    parser.add_argument('--url', default='http://localhost:5050', help='Base URL')
    parser.add_argument('--track', help='Test single track')
    parser.add_argument('--ms-only', action='store_true', help='Test only middle school')
    parser.add_argument('--hs-only', action='store_true', help='Test only high school')
    args = parser.parse_args()

    agent = TestAgent(args.url)

    if args.track:
        # Single track
        is_ms = args.track in MS_TRACKS
        grade = MS_GRADES.get(args.track) or HS_GRADES.get(args.track, 11)
        event = MS_EVENT if is_ms else HS_EVENT
        agent.run_full_flow(args.track, grade, event, is_ms)
    else:
        # All tracks
        if not args.ms_only:
            for track in HS_TRACKS:
                agent.run_full_flow(track, HS_GRADES[track], HS_EVENT, False)
        if not args.hs_only:
            for track in MS_TRACKS:
                agent.run_full_flow(track, MS_GRADES[track], MS_EVENT, True)

    agent.print_summary()


if __name__ == '__main__':
    main()
