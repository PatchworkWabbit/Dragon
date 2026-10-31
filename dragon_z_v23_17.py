# ============================================================
# DRAGON Z v23.17 - built up from the zero gate (safe mode)
# ============================================================
# OWNERSHIP: Dragon Z is Luke's engine. The rules, the design, the ideas and
# the direction are Luke's, and so is everything it finds. Nobody else is
# named in it and nobody else claims any of it.
# ============================================================
# v23.1 (part 1 of 3): the archive is checked from 0 BEFORE any work or save. A file that fails is kept
#   under its own name and is never written over a good backup. The replay reports damage instead of
#   crashing or hanging. A typed fraction past the counter, and a negative selector, are kept in the
#   wanted archive. A bad command no longer ends the run. v23 has its own memory file.
# v23.3 (part 2 of 3, rebuilt; v23.2 was withdrawn because it touched undo): the replay now also checks the clock stamps, run numbers, rule text, every cursor,
#   the role names, why each role exists and which record it points at. Interrupt (Ctrl-C) stops at a clean
#   boundary and saves a whole state. Search bounds are saved in each record. Late templates are no longer
#   starved. Fractions typed before they are found are kept as wants. A way back that ends in a move the engine
#   itself blocks (0/x, x/0) is kept in a library of its own, the DEADLOCKS, through Z0. The cores, undo
#   included, are untouched. Wording: 'among the N tried', '-(1 + 1/2)'.
# v23.4: the solve command finishes the work already in hand (no new counter records, no new pairs). Every
#   deadlock keeps a watch of the zero split: it was run for a fixed number of steps and never closed.
# v23.5: tangents. Every branch off a main path (a turn then a step, or a step back against a unit) is kept
#   once in a library of its own, through Z0, with where it lands. When a full pass over the walked pairs
#   keeps no new branch, pair exploration pauses and saves until something new arrives.
# v23.6: a pair typed by hand is marked, like every other typed record, so the replay can check the pair
#   cursor exactly. A reset cursor can no longer make the engine walk the same pairs twice unseen.
# v23.7 (part 3, step 1): typed equations accept negative numbers (x+2=-3, -3+x=5) and x=5 is understood;
#   the slot replay no longer skips its later checks once it has 20 problems; the three look-up caches are
#   tied to the archive they were built from; the provenance list now names the Python arithmetic left in
#   the engine (template str()/int(), negation in rational, the 10**9 'no limit', subtraction read-outs).
# v23.8 (part 3, step 2): every change to a stored record is a new Z0 stamp. step (the nxt link), retry_slots
#   (limit, need) and retry_products (limit, tries) are wrapped, not edited: the wrapper calls the core as it
#   is and stamps what changed. The replay checks each record against its stamped history.
# v23.8.1: each slot retry stamp carries its own retry count (try 1, 2, 3 ...), as products already do, so the
#   replay can see a stamp that is missing from a slot's history.
# v23.10 phone (part 3, step 4): every inner step - S, the unit step, the turn and the unit turn - is counted as it
#   happens and handed to Z0 in batches, before each replay and save. Z0 reaches the same numbers as v23.9 NOT FOR
#   PHONES without a gate passage per step, so a run costs little more than v23.8.1. The replay switches the counting
#   off while it checks.
# v23.11 (part 3, step 5): the archive is saved compressed (gzip), about 6 times smaller, and nothing is dropped.
#   The file is dragon_z_v23_memory.json.gz and its backup is dragon_z_v23_memory.json.gz.bak. A plain
#   dragon_z_v23_memory.json from the earlier versions is read once if no compressed file exists; it is never
#   changed or deleted. The command  export  writes a readable copy of the archive (the engine never reads it).
# v23.12 (part 3, step 6): the archive is replayed from 0 ONCE per launch, at start-up. Before saving, a light check
#   runs instead of a second full replay: everything is rechecked except the blank searches and products that are
#   unchanged since the start-up replay passed (each is matched by a fingerprint). Anything new or changed is
#   re-solved from S. If the light check ever fails, the full replay gives the verdict. The command  replay  (or
#   check) is still the full re-check from 0, whenever you want it.
# v23.13: nobody but Luke is named in the engine. Corrections that were labelled with another name now carry
#   the Dragon Z version it was fixed in. In an older archive those labels are changed on the first launch, each change as a Z0 stamp.
# v23.14: approaches. A path that closes in on a value without ever arriving (1/1, 1/2, 1/3 ... gets nearer to
#   0 at every step and never reaches it) is kept in a library of its own, the APPROACHES, through Z0, apart from
#   the deadlocks (stuck paths), the tangents and the other kept records. The test lets the gap wobble: the best gap
#   keeps improving, the last gap is the smallest yet and smaller than the first, and the target is never reached or
#   crossed. The target is the lowest value the engine holds. The length is whatever the divisions already
#   made give (no new typed number). Nothing is edited in the cores: the library only reads the divisions.
# v23.15: the LIMIT role. The first time the engine keeps a path that closes in on a value without arriving (an
#   approach), it writes down the role limit, pointing at that approach, with its recipe. Nothing is programmed in:
#   the role is earned from the engine's own records, like add and multiply. An archive that already holds
#   approaches but no limit role is given the role once, as a stamped record.
# v23.16: the DIFFERENCE role. For one counted number a, the products a x b and a x (b+1) sit side by side in the
#   archive. The engine climbs from the smaller to the larger with S alone, counts the steps, and keeps that
#   change in a library of its own, the DIFFERENCES, through Z0. Where the change is nothing it is kept too. The first
#   time a change is more than nothing, the role difference is written down, pointing at that record. An older archive
#   fills its library over the next runs; the role is written once. No core is edited: the library only reads products.
# v23.17: the GROUP role (stacking smaller parts onto a bigger whole). The engine takes the counted numbers 1, 2,
#   3 ... one at a time and stacks each part onto the whole made so far, climbing with S alone. Each stack is kept
#   in a library of its own, the TOTALS, through Z0, and each total is built on the one before it. The first time a part
#   is stacked onto a whole that already holds parts, the role group is written down, pointing at that record. An older
#   archive fills its library over the next runs. No core is edited: the library only reads the counter.
# Plain Python 3. No SymPy, no extra installs. Runs in Pydroid3.
#
# What is in v3 (and ONLY this):
#   Z0  the zero gate. Every step and every record passes through it.
#   S   the counter. The only number-maker. 0 -> 1 -> 2 -> 3 ...
#   Addition is NOT given. It emerges from S:
#     the engine takes every pair of counted numbers (a, b) and walks S
#     forward b times from a. Where the walk lands is kept as an expression.
#     The first time a walk of one or more S steps lands, the engine writes
#     down a ROLE ("repeat S by a count") - that is addition being found.
#     Every pair is walked, both orders, zero included, repeats included.
#     If a walk goes past the end of the counter, it makes the counter longer.
#   i is GIVEN as an action, the turn: it rotates the direction S walks in,
#     +1 -> +i -> -1 -> -i -> +1. Nothing else about i is given.
#     At every point of a walk the engine can take an S step OR an i turn,
#     and it explores both, every time: S then more S, S then a turn, a turn
#     then S, a turn then another turn. Whatever comes first comes first.
#     A step taken in a turned direction lays a unit of that direction.
#     A unit that meets its opposite cancels, and both go back to Z0.
#     That cancelling IS subtraction, and a walk left holding -1 is a
#     negative. Neither is given. The engine writes down each as a role the
#     first time it happens.
#   00404 is GIVEN as the first slot template, and every counted number is a
#     template too (its digits). A digit c becomes c units (1111 for a 4) and a
#     0 stays a 0. Between every two symbols sits a SLOT. Each slot is filled
#     with 'join' (glue the symbols into one number) or with an operation
#     the engine has already FOUND: + (found from S) or - (found from the i
#     turn). Slots wait until both have been found. Every filling is tried,
#     none is skipped, unused slots are allowed (a slot left on 'join' just
#     glues), and every result is kept, zero included. Operations used in a
#     slot are walked with S steps and i turns, never with Python's + or -.
#   Multiplication is NOT given either. It emerges from repeating addition:
#     for every pair of counted numbers (a, b) the engine also repeats the
#     add of a, b times, starting from nothing. The first time that happens
#     with b of two or more, it writes down a ROLE: multiply. Zero counts:
#     0 x 2 = 0 is a real path and is kept like every other.
#     The same pair also gets its units TURNED b times (every unit of a takes
#     b i-turns). The first time that changes the number, the engine writes
#     down the role: rotate. Four turns bring a back to a, so rotating by a
#     whole number only ever lands on a, i*a, -a or -i*a. It is the same
#     trick as three left turns making a right turn: a few of the basic
#     actions in a row become a new action of their own.
#   The engine also writes down the turn combinations it meets:
#     two turns in a row (half_turn), three (right_turn) and four (full_turn,
#     which brings it back to the start, so the turns cancel back to Z0).
#   Once multiply is found, slots may hold * as well. The usual order is used:
#   * first, then + and - left to right. Products need the counter to be long
#     enough to hold the result, otherwise they are parked and retried.
#   Division is NOT given. It emerges from SPLITTING, the way 00404 does:
#     00404 is units and zeros: 1111 0 1111 is eight units split by a 0 into
#     two groups of four. For every pair (a, b) the engine lays out a units
#     (S steps), and every time b of them are in a row it puts a 0 after
#     them - a split - and counts the group with S. The groups it counted are
#     the answer, the units left over are the remainder, and a remainder over
#     b is a fraction. Nothing is divided: it is only laid out, split and
#     counted. The first time a 0 is put in, the engine writes down the role
#     divide. The first time units are left over, it writes down: remainder.
#     Dividing by zero cannot be laid out; that record is kept as blocked.
#     Turn the units first (T) and the same split divides negatives and i.
#   Fractions are NOT given. They emerge from the leftovers of splitting:
#     when units are left over after the last full group, those leftover units
#     are a PART of a group: r units out of a group of b. That part is a
#     fraction. 7 split into groups of 2 leaves 1 unit of 2: 3 and 1/2.
#     The same part can be written many ways (1 of 2, 2 of 4, 3 of 6). The
#     engine finds that for itself by splitting again: it keeps splitting the
#     group by its leftover (a chain of leftovers) until nothing is left over.
#     The last group size that fits both is the common group g, and splitting
#     the leftover and the group by g gives the same fraction in fewest parts.
#     First fraction found: role fraction. First time a fraction is written
#     the same way in fewer parts: role reduce. Look up 1/2 or 7/2 to see them.
#   Once divide and fractions are found, slots may hold / as well (v11).
#     A slot result is now a number OR a fraction. Every operation in a slot
#     goes through Z0 as one passage ('rational') and is worked out from the
#     engine's own pieces: adding and taking away are S walks (signed), a
#     product is repeated adding, a quotient is a split and regroup, and a
#     fraction is always written in fewest parts by the leftover chain. The
#     usual order is used: * and / first, left to right, then + and -.
#     A group of nothing (/0) can never be laid out: that filling is kept
#     as BLOCKED, never dropped. Anything that outgrows the counter is parked.
#   x is NOT given as algebra (v12). x is a BLANK, a place where a number goes.
#     Once every operation has been found, the engine takes each pair of
#     counted numbers (a, c) and asks, in 8 shapes, which numbers can fill the
#     blank: a+x=c, x+a=c, a-x=c, x-a=c, a*x=c, x*a=c, a/x=c, x/a=c.
#     It does NOT solve. It TRIES: x = 0, 1, -1, 2, -2, 3 ... (counted up with S
#     and taken away from 0 for the negatives), works the sum out with the same
#     operations the slots use, and keeps every x that makes it true. Each
#     try goes through Z0. How far it tries comes from the engine's own
#     progress: no further than the counter, and no further than a+c+2.
#     Where nothing fits, that is kept too. The engine writes down a role the
#     first time it meets: unknown (some x fits), negative_answer, any_answer
#     (every x fits, like 0*x=0), no_answer, and undo_add / undo_subtract /
#     undo_multiply / undo_divide - the first time the x that fits is also what
#     you get by going BACKWARDS (take c away by a, regroup c by a, ...). Undoing
#     is not given: it is found when going backwards lands on the same x.
#   The PLANE (v13). Nothing new is given: every path of S steps and i turns
#     already ends on a point, real part and i part. The engine now keeps
#     every distinct point it has reached as a plane record, in the order it
#     was first reached, stamped through Z0, with the first path that got
#     there and which axis or quadrant it sits in. The first point with BOTH
#     a real part and an i part writes down the role plane (two dimensions
#     from one line), and the first point in each quarter writes down
#     quadrant_1 (+,+) quadrant_2 (-,+) quadrant_3 (-,-) quadrant_4 (+,-).
#     To SEE its dimensions the engine LOOKS: it walks out from Z0 with S
#     steps (and takes away for the other way) to place the grid, marks
#     O for Z0, # for a point it has reached and . for one it has not. Every
#     look passes through Z0 and is kept with the picture and the moment.
#   NOT FOUND is an archive too (v14). Every time a lookup comes back empty
#     (a counter number not reached, a point no path has reached, a point the
#     plane has not seen, a blank not tried, a slot value or fraction nothing
#     has made yet) the engine writes it into the WANTED archive: stamped through
#     Z0 with an id, recipe and clocks, and a count of how many times it was
#     asked. Nothing is dropped. Every run, and before every save, the engine
#     checks every open want against what it has built since. The moment
#     something answers it, the want is marked FOUND with a pointer to what
#     answered it and the run it happened in. Looking the same thing up again
#     says so ("wanted before..."). Commands: wanted, wanted found.
#   x ON THE PLANE (v15). The blank now reaches the i turns and the whole plane.
#     The pairs are POINTS the plane has reached, not only counted numbers, so
#     i * x = 1 and (2+3i) + x = 0 are asked like any other. The engine tries
#     every plane point it has already reached, near Z0 first, in the same 8
#     shapes, and keeps every point that makes the sum true. Sums on the plane
#     are worked out from the engine's own pieces: adding and taking away are
#     S walks on each part, a product repeats adds and each i times i is two
#     turns (a half turn, which is -1), and a quotient is a split and regroup.
#     Going backwards is tried too. The roles written down the first time they
#     happen: imaginary_answer (an x that is a pure i number), complex_answer
#     (an x with both parts), every_point (every point tried fits), and
#     undo_turn - the x found is what turning the answer back gives, like
#     i * x = 1 giving x = -i, three turns on. Points not yet reached are not
#     tried, and a blank nobody has tried goes into the wanted archive.
#     Commands: solve i*x=1 (try a blank on the plane now).
#   THE SLOTS REACH THE i TURNS AND THE PLANE (v16).
#     1. A new slot choice, T (turn): a T b turns a, b times. It waits for the
#        role rotate to be found. (v18: the turns are taken one at a time.)
#     2. Slot numbers can hold i. In a template a symbol i is a turn marker:
#        joined symbols 11i read as 11 turned once (11i), i alone is i, ii is -1.
#     3. Every plane point with an i part becomes a template of its own, written
#        3i2 for 3+2i (the digits of each part with an i between), so the slots
#        can build on points the plane has reached.
#     4. A slot answer can now be a point. + - * / on points are worked out with
#        the same pieces as the plane blanks. A fraction meeting an i, a turn
#        count that is not a whole number of turns, or a quotient that is not a
#        whole point is BLOCKED and kept with the reason, never dropped.
#     5. Every point a slot lands on says where it sits on the plane and whether
#        the paths have reached it. Look a point up (3+2i) to see the slot
#        fillings that made it.
#   x IN THE SLOTS, AS A PROOF (v17). x is never forced onto an expression.
#     Two ways it appears: (1) a NEW EQUATION is one you write (solve i*x=1),
#     and the engine only tries it. (2) a PROOF is where an expression is
#     already related: every slot filling is a true statement, like 1+11 = 12.
#     The engine hides one number in it (1+x = 12) and tries the plane points it
#     has reached for the x that makes it true again, in the same slot sums.
#     It keeps WHAT IT FOUND: whether the number it hid came back, and any other
#     x that fits too. It also keeps when the hidden number is out of reach (not
#     reached yet or too far away). Blocked fillings are kept as blocked. Roles:
#     proof (the hidden number came back), other_answer (another x fits too),
#     lost_answer (the hidden number did not come back). New in the plane
#     blanks: undo_zero, so a zero answer that going backwards agrees with is
#     named as well - zero is never skipped.
#     Commands: proofs, prove 42 1 (slot filling 42, hide its number 1).
#   TWO SHORTCUTS REMOVED (v18). Nothing here is new maths; it is two places
#     where v17 did the work for the engine, and now the engine does it.
#     1. FEWEST PARTS. The chain 'split the group by its leftover, then split
#        THAT by its leftover, until nothing is left' is no longer a function
#        written for the engine. Every pair has already been split and kept in
#        the divisions archive, so the engine FOLLOWS ITS OWN RECORDS: it looks
#        up the division of the group by the leftover, reads that leftover,
#        looks up the next one, and stops at the record with nothing left over.
#        Each fraction now carries the division records it followed (chain).
#        The last divisor is the common group. (The slot sums still use a plain
#        helper to keep their fractions small. Only the fractions archive and
#        the role reduce are earned by following records.)
#     2. TURNS. The T slot choice no longer cuts the turn count down by fours.
#        It turns the units one turn at a time, b times. Five turns landing
#        where one turn does is now something the engine does by turning, and
#        1T1 and 1T5 both fitting a blank shows it.
#   TWO MORE SHORTCUTS REMOVED (v19), found by auditing v18 for places where
#     Python did the engine's counting.
#     1. A joined group of template symbols (like 1111 or 0011) used to be read
#        with Python's int(). Now it is COUNTED: for each symbol the number so
#        far is repeated-added ten times (place value, from the multiply that was
#        found) and a 1 takes one S step. A group the counter has not reached is
#        PARKED, as before, and retried when the counter grows.
#     2. Marks of i in a template used to be cut down with a remainder by four.
#        Now every i mark is one literal turn of the units.
#     Still Python, on purpose and named here so nothing hides: the signs and
#     sizes it checks (is it below zero, is it zero), how far the blank and the
#     proofs try (phone-safety limits), the order the cursors walk, and the method
#     of each backwards step. The procedures (repeat the add, split and regroup,
#     walk back) are code written with an AI coding tool from the rules Luke set. What the
#     engine earns is every result, every role name, every recipe and every record.
#   PROVENANCE (v20). Type provenance and the engine prints, for every
#     capability, three separate things so credit is never blurred:
#       RULE      the idea and the rule - Luke's
#       PROCEDURE the function written with the coding tool to carry the rule out
#       EARNED    what the engine itself produced: the role (written on first
#                 sighting, with its run and recipe) and the records behind it
#     It reads the live archives, so EARNED is always checked, never claimed.
#     Nothing in it is a record; it is a report.
#   CORRECTIONS (v21). Every error that was caught is kept, never hidden: what
#     was wrong, who caught it (Luke, the tests, or the Dragon Z version), and how it was
#     fixed. The errors from v2 to v20 are written in on the first launch, and
#     a replay fails if any of them is edited or removed. Add a new one with
#         correction WHO | WHAT WAS WRONG | HOW IT WAS FIXED
#     (WHO is Luke, tests or a Dragon Z version such as Dragon Z v23.1). Type corrections to see them all.
#   EVERY RECORD is stamped with everything the engine knows about it:
#       z0     its passage number through Z0 in its own archive
#       gid    its global id: one number, shared by every kind of record
#       fam    which archive it belongs to
#       run    which run made it
#       t      the four clocks: zero tick, session, wall time, elapsed, CPU
#       recipe the S steps and i turns that make it (not only roles any more)
#   Type  who 1234  to find ANY record by its global id.
#   RECIPES: every role the engine finds is saved with the exact combination of
#   S steps and i turns that made it emerge. Written as a short word:
#       S*3      three S steps          I*2     two i turns
#       T        one i turn of every unit of a number
#       [S*2]x3  add (S*2) again and again, 3 times
#   S*0 means zero steps were taken: the walk stayed at Z0. Type recipes to see
#   them all, or look up any value: each way of reaching it shows its recipe.
#   E (energy) is NOT in yet. It goes in after the S core is finished.
#   No digits, no + - * /. Everything else must emerge, one careful step at
#   a time on top of this.
#
# How it works, in plain words:
#   1. The engine starts with 0 only (it is record #0, "Z0").
#   2. Each step takes the newest number and asks S for the next one.
#      The step goes through Z0 and the new record goes through Z0.
#   3. Everything is kept and saved. Nothing is rejected or skipped.
#   4. Every launch the engine re-checks its whole archive on its own
#      (REPLAY). If the archive was damaged or edited, it says so.
#   5. Each run continues exactly where the last one stopped.
#
# Its memory file is separate, so no older engine's file is touched.
# This is a computational exploration, not a mathematical proof.

import json
import gzip
import hashlib
import zlib
import signal
import os
import sys
import time

# ---------------- SETTINGS (change freely) ----------------
WORK_PER_RUN = 1000          # S steps taken each run (phone-safety only)
CLOCKS_ON = True             # stamp every record with the four clocks
BACKUP_ON_SAVE = True        # keep the previous good save as <memory>.bak
PAIR_WORK_PER_RUN = 1000     # pairs walked each run (phone-safety only)
MUL_WORK_PER_RUN = 1000      # pairs multiplied/rotated each run (phone-safety only)
TURN_WORK_PER_RUN = 1000     # S-or-turn expansions each run (phone-safety only)
SLOT_WORK_PER_RUN = 200      # slot fillings tried each run (phone-safety only)
MEMORY_FILE = 'dragon_z_v23_memory.json.gz'          # saved compressed
LEGACY_FILE = 'dragon_z_v23_memory.json'             # the plain file of v23.1 to v23.10: read once, never changed
EXPORT_FILE = 'dragon_z_v23_memory.export.json'      # a readable copy made by the export command
GZIP_LEVEL = 6
PROOF_WORK_PER_RUN = 40     # proof searches per run (phone-safety only)
PROOF_BOUND = 60            # furthest from Z0 a proof tries (phone-safety only)
XP_WORK_PER_RUN = 30         # plane pairs searched for an unknown each run (phone-safety only)
XP_BOUND = 8                 # how far from Z0 the blank is tried (phone-safety only)
PLANE_WORK_PER_RUN = 20000   # path nodes looked at for new plane points each run (phone-safety only)
X_WORK_PER_RUN = 60          # pairs (a, c) searched for an unknown each run (phone-safety only)
FRAC_WORK_PER_RUN = 1000     # divisions looked at for leftovers each run (phone-safety only)
DIV_WORK_PER_RUN = 1000      # pairs split and regrouped each run (phone-safety only)
# -----------------------------------------------------------

import re
from functools import lru_cache

VERSION = 'v23.17'
ZERO_RULE = 'everything_through_zero_dragon_v21'
PROOF_RULE = 'hide_one_number_and_find_it_v1'
XP_ROLE_RULE = 'blank_on_the_plane_v1'
PLANE_RULE = 'point_seen_off_the_line_v1'
X_ROLE_RULE = 'blank_filled_by_trying_v1'
FRAC_ROLE_RULE = 'leftover_part_of_group_v1'
DIV_ROLE_RULE = 'split_and_regroup_v1'
MUL_ROLE_RULE = 'repeat_action_by_count_v1'
SLOT_RULE = 'slot_template_given_v1'
SLOT_TEMPLATE = '00404'
OP_ROLES = (('add', '+'), ('subtract', '-'), ('multiply', '*'), ('divide', '/'), ('rotate', 'T'))   # slots may use these once the role is found
SLOT_OPS = [sym for _, sym in OP_ROLES] + ['join']     # operations first, so early fillings stay small
SLOT_SIG = ''.join(SLOT_OPS)
I_ACTION_RULE = 'i_turn_action_given_v1'
TURN_ROLE_RULE = 'emerged_on_first_sighting_v1'
ADD_ROLE_RULE = 'repeat_S_by_count_v1'


def legacy_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), LEGACY_FILE)


def export_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), EXPORT_FILE)


def memory_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), MEMORY_FILE)


# ---------------- the four clocks ----------------
# 1. Zero tick     - how many times anything has passed through Z0.
# 2. Wall clock    - the real date and time.
# 3. Elapsed clock - time since this session started; never goes backwards.
# 4. CPU clock     - processor time used this session.
# Elapsed and CPU restart every session, so each stamp also names its session.

SESSION = {'id': None, 'mono0': time.monotonic_ns(), 'cpu0': time.process_time_ns()}


def clock_state(m):
    return m.setdefault('clock', {'sessions': 0})


def start_session(m):
    c = clock_state(m)
    c['sessions'] += 1
    SESSION.update(id=c['sessions'], mono0=time.monotonic_ns(),
                   cpu0=time.process_time_ns())


def read_clocks(m):
    """[zero tick, session, wall ms, elapsed microseconds, CPU microseconds]"""
    return [zero_state(m)['passages'], SESSION['id'], time.time_ns() // 1000000,
            (time.monotonic_ns() - SESSION['mono0']) // 1000,
            (time.process_time_ns() - SESSION['cpu0']) // 1000]


def clock_line(t):
    return ('zero tick %d | %s | %.3f s elapsed, %.3f s CPU into session %d'
            % (t[0], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t[2] / 1000)),
               t[3] / 1e6, t[4] / 1e6, t[1]))


# ---------------- ZERO GATE (Z0) ----------------
# Everything that comes from 0 goes back through 0.
# Passing through 0 never changes a value or a path. It records that the
# path went through Z0, in order, with the clocks.

def zero_state(m):
    return m.setdefault('zero', {'rule': ZERO_RULE, 'nexus': 'Z0',
                                 'passages': 0,          # every passage of any kind
                                 'gids': 0,              # global ids handed out, all archives
                                 'division_passages': 0, # split-and-regroup records stamped
                                 'fraction_passages': 0, # leftover parts stamped
                                 'plane_passages': 0,    # plane points stamped
                                 'proof_passages': 0,    # slot proofs stamped
                                 'correction_passages': 0,   # caught errors stamped
                                 'deadlock_passages': 0,     # ways back that hit a blocked move stamped
                                 'tangent_passages': 0,      # branches off main paths stamped
                                 'approach_passages': 0,     # paths that close in without arriving stamped
                                 'difference_passages': 0,   # changes between neighbouring products stamped
                                 'total_passages': 0,        # parts stacked onto a whole stamped
                                 'pair_marks': 1,            # typed pairs are marked (1 = this file knows it)
                                 'change_stamps': 1,         # every change to a record is stamped (1 = this file knows it)
                                 'punknown_passages': 0, # plane blank searches stamped
                                 'want_passages': 0,     # not-found wants stamped
                                 'view_passages': 0,     # looks at the plane stamped
                                 'unknown_passages': 0,  # blank searches stamped
                                 'record_passages': 0,   # counter records stamped
                                 'expression_passages': 0,   # walked pairs stamped
                                 'role_passages': 0,     # discovered roles stamped
                                 'node_passages': 0,     # S-or-turn path nodes stamped
                                 'slot_passages': 0,     # slot fillings stamped
                                 'product_passages': 0,  # repeated adds and repeated turns stamped
                                 'operations': {},       # how often each operation ran
                                 'late_passages': 0})


def S(n):
    """The counter. The only number-maker in v1. Natural numbers only."""
    return n + 1


def turn(d):
    """The i action. Rotates the walking direction: +1 -> +i -> -1 -> -i -> +1."""
    return (d + 1) % 4


def unit_step(c, d):
    """One S step taken in direction d. The unit laid meets its opposite if one
    is already there: both cancel (back to Z0). Otherwise the unit is laid."""
    c = list(c)
    o = (d + 2) % 4
    if c[o] > 0:
        c[o] -= 1
        return c, True
    c[d] += 1
    return c, False


def signed_walk(x, b, d):
    """Walk b S steps from the signed number x, facing +1 (d=0, adding) or
    -1 (d=2, taking away). Units that meet their opposite cancel. Returns the
    signed number reached."""
    c = [x, 0, 0, 0] if x >= 0 else [0, 0, -x, 0]
    for _ in range(b):
        c, _gone = unit_step(c, d)
    return c[0] - c[2]


def repeat_add(a, b, limit=None):
    """Add a, b times, starting from nothing. Every add is walked with S steps.
    If the total reaches `limit` (the length of the counter) it stops and
    returns None: the answer is not countable yet."""
    acc = 0
    for _ in range(b):
        acc = signed_walk(acc, a, 0)
        if limit is not None and acc >= limit:
            return None
    if limit is not None and acc >= limit:
        return None
    return acc


def turn_units(c):
    """One i turn of every unit: +1 units become +i, +i become -1, and so on."""
    return [c[3], c[0], c[1], c[2]]


def repeat_turn(a, b):
    """Turn every unit of a, b times. Returns [real, imaginary]."""
    c = [a, 0, 0, 0]
    for _ in range(b):
        c = turn_units(c)
    return [c[0] - c[2], c[1] - c[3]]


def regroup(a, b):
    """Lay out a units one at a time. Every time b of them are in a row, the
    group is counted with S and, if units remain, a 0 is put in to split it off.
    Returns (groups counted, units left over, zeros put in), or None if b is 0:
    a group of no units can never fill."""
    if b == 0:
        return None
    groups = run = zeros = 0
    for placed in range(a):
        run = S(run)
        if run == b:
            groups = S(groups)
            run = 0
            if placed + 1 < a:
                zeros = S(zeros)
    return groups, run, zeros


def reduce_part(r, b):
    """The leftover r (1 or more, fewer than b) is a part of a group of b.
    Split the group by the leftover, then split THAT group by its leftover, and so
    on until nothing is left over. The last group size that fits is g. Splitting r
    and b by g writes the same part in fewest parts.
    Returns (g, r over g, b over g, how many splits it took)."""
    x, y, steps = b, r, 0
    while y:
        _groups, leftover, _zeros = regroup(x, y)
        x, y = y, leftover
        steps = S(steps)
    return x, regroup(r, x)[0], regroup(b, x)[0], steps


def rational(op, a, b, limit):
    """One slot operation on two numbers, each a (numerator, denominator) pair.
    Built only from the engine's own pieces: signed S walks (adding / taking away),
    repeated adding (products), split-and-regroup (quotients) and the leftover chain
    (fewest parts). Returns a reduced pair, None if the counter is too short, or
    'DIV0' when a group of nothing was asked for."""
    def big(x):
        return abs(x) >= limit

    def times(x, y):
        if x == 0 or y == 0:
            return 0
        r = repeat_add(abs(x), abs(y), limit)
        if r is None:
            return None
        return r if (x < 0) == (y < 0) else signed_walk(0, r, 2)

    def plus(x, y):
        return signed_walk(x, abs(y), 0 if y >= 0 else 2)

    (n1, d1), (n2, d2) = a, b
    if op == '/':
        if n2 == 0:
            return 'DIV0'
        n, d = times(n1, d2), times(d1, abs(n2))
        if n is not None and n2 < 0:
            n = signed_walk(0, abs(n), 2) if n > 0 else abs(n) and signed_walk(0, abs(n), 0)
    elif op == '*':
        n, d = times(n1, n2), times(d1, d2)
    else:
        x, y, d = times(n1, d2), times(n2, d1), times(d1, d2)
        if x is None or y is None or d is None:
            return None
        n = plus(x, y) if op == '+' else plus(x, -y)
    if n is None or d is None or big(n) or big(d):
        return None
    if n != 0 and d != 1:
        g, rr, bb, _s = reduce_part(abs(n), d)
        n, d = (rr if n > 0 else signed_walk(0, rr, 2)), bb
    if n == 0:
        d = 1
    return (n, d)


UNKNOWN_FORMS = (('+', 'R'), ('+', 'L'), ('-', 'R'), ('-', 'L'),
                 ('*', 'R'), ('*', 'L'), ('/', 'R'), ('/', 'L'))      # R: a op x = c    L: x op a = c
UNDO_ROLE = {'+': 'undo_add', '-': 'undo_subtract', '*': 'undo_multiply', '/': 'undo_divide'}


def undo(op, side, a, c):
    """Go BACKWARDS from c with the engine's own pieces: take away, put back, regroup,
    repeat add. Returns the number reached, or None if going backwards gets nowhere."""
    if op == '+':
        return signed_walk(c, a, 2)                          # take a away from c
    if op == '-':
        return signed_walk(a, c, 2) if side == 'R' else signed_walk(c, a, 0)
    if op == '*':
        if a == 0:
            return None
        q, rem, _z = regroup(c, a)
        return q if rem == 0 else None                       # c split into groups of a
    if side == 'R':                                          # a / x = c
        if c == 0:
            return None
        q, rem, _z = regroup(a, c)
        return q if rem == 0 else None
    return repeat_add(c, a)                                  # x / a = c: c, a times


def look(r, reached, fmt=2):
    """Walk out from Z0 to place the grid, then mark what has been reached.
    O = Z0, # = a point the engine has reached, . = one it has not."""
    ax = [signed_walk(0, k, 2) for k in range(r, 0, -1)] + [0] + [signed_walk(0, k, 0) for k in range(1, r + 1)]
    seen = set(tuple(p) for p in reached)
    rows = []
    if fmt == 1:                     # the v13/v14 drawing, kept so old looks still redraw the same
        for y in reversed(ax):
            label = '%+d' % y if y else ' 0'
            cells = ' '.join('O' if (x, y) == (0, 0) else '#' if (x, y) in seen else '.' for x in ax)
            rows.append('%4si  %s' % (label, cells))
        rows.append('      ' + ' '.join(('%d' % abs(x))[-1] for x in ax) + '   (real part; left of the centre is negative)')
        return rows
    for y in reversed(ax):
        label = '%+d' % y if y else '0'
        cells = ''.join('  O' if (x, y) == (0, 0) else '  #' if (x, y) in seen else '  .' for x in ax)
        rows.append('%4si %s' % (label, cells))
    rows.append('      ' + ''.join('%3d' % x for x in ax) + '   (real part)')
    return rows


BLOCKS = ('DIV0', 'MIXED', 'NONINT')
BLOCK_WHY = {'DIV0': 'a group of nothing can not be laid out',
             'MIXED': 'a fraction met an i, or a turn count that is not whole turns',
             'NONINT': 'the quotient is not a whole point'}


def slotop(op, a, b, limit):
    """One slot operation. a and b are (real part, i part, denominator).
    T turns every unit of a, one turn at a time, b times."""
    (ar, ai, ad), (br, bi, bd) = a, b
    if op == 'T':
        if bd != 1 or bi != 0 or br < 0 or ad != 1:
            return 'MIXED'
        c = [max(ar, 0), max(ai, 0), max(-ar, 0), max(-ai, 0)]
        for _ in range(br):                         # one i turn at a time: +1 -> +i -> -1 -> -i -> +1
            c = turn_units(c)
        return (c[0] - c[2], c[1] - c[3], 1)
    if ai == 0 and bi == 0:
        res = rational(op, (ar, ad), (br, bd), limit)
        if res is None or res == 'DIV0':
            return res
        return (res[0], 0, res[1])
    if ad != 1 or bd != 1:
        return 'MIXED'
    res = cplx(op, (ar, ai), (br, bi), limit)
    return (res[0], res[1], 1) if isinstance(res, tuple) else res


def cplx(op, A, B, limit):
    """One sum on the plane. A and B are (real part, i part). Built from S walks,
    repeated adds, turns (i times i = two turns = take away) and split-and-regroup.
    Returns a point, None if the counter is too short, 'DIV0', or 'NONINT' when the
    quotient is not a whole point."""
    def times(x, y):
        if x == 0 or y == 0:
            return 0
        r = repeat_add(abs(x), abs(y), limit)
        if r is None:
            return None
        return r if (x < 0) == (y < 0) else signed_walk(0, r, 2)

    def plus(x, y):
        return signed_walk(x, abs(y), 0 if y >= 0 else 2)

    def away(x):
        return signed_walk(0, abs(x), 2 if x > 0 else 0)

    (a, b), (c, d) = A, B
    if op in '+-':
        re_ = plus(a, c if op == '+' else away(c))
        im = plus(b, d if op == '+' else away(d))
    else:
        if op == '*':
            ac, bd, ad, bc = times(a, c), times(b, d), times(a, d), times(b, c)
            if None in (ac, bd, ad, bc):
                return None
            re_, im = plus(ac, away(bd)), plus(ad, bc)           # i * i = two turns = taking away
        else:
            n1, n2 = times(c, c), times(d, d)
            if n1 is None or n2 is None:
                return None
            norm = plus(n1, n2)
            if norm == 0:
                return 'DIV0'
            ac, bd, bc, ad = times(a, c), times(b, d), times(b, c), times(a, d)
            if None in (ac, bd, bc, ad):
                return None
            parts = []
            for top in (plus(ac, bd), plus(bc, away(ad))):
                q, rem, _z = regroup(abs(top), norm)
                if rem:
                    return 'NONINT'
                parts.append(q if top >= 0 else away(q))
            re_, im = parts
    if abs(re_) >= limit or abs(im) >= limit:
        return None
    return (re_, im)


def undo2(op, side, A, C):
    """Go BACKWARDS on the plane: take away, put back, regroup, turn back. Returns a point or None."""
    big = 10 ** 9
    def ok(r):
        return r if isinstance(r, tuple) else None
    if op == '+':
        return ok(cplx('-', C, A, big))
    if op == '-':
        return ok(cplx('-', A, C, big)) if side == 'R' else ok(cplx('+', C, A, big))
    if op == '*':
        return ok(cplx('/', C, A, big))
    return ok(cplx('/', A, C, big)) if side == 'R' else ok(cplx('*', C, A, big))


PRIMITIVES = {'S': S, 'group': lambda digits, limit: group_point(digits, limit), 'slotop': slotop, 'rational': rational, 'undo': undo, 'look': look, 'cplx': cplx, 'undo2': undo2, 'I': turn, 'Sd': unit_step, 'signed_walk': signed_walk,
              'repeat_add': repeat_add, 'repeat_turn': repeat_turn, 'regroup': regroup,
              'reduce': reduce_part}


def walk(m, start, count):
    """Follow S forward `count` times from counter record `start`.
    Uses only the S links between records. If the walk reaches the end of the
    counter, S makes the counter longer. Returns the record id it lands on."""
    recs = m['records']
    n = start
    for _ in range(count):
        if recs[n].get('nxt') is None:      # n is the newest: S makes the next one
            step(m)
        n = recs[n]['nxt']
    return n


def zero_gate(m, what, **kw):
    """The single gate. what = 'operation' or 'record'.
    record families: 'record' (counter), 'expression', 'role'."""
    z = zero_state(m)
    z['passages'] += 1
    if what == 'operation':
        name = kw['name']
        z['operations'][name] = z['operations'].get(name, 0) + 1
        if name == 'repeat_S':
            return walk(m, *kw['args'])
        return PRIMITIVES[name](*kw['args'])
    if what == 'record':
        rec = kw['record']
        if 'z0' in rec:
            return rec                      # already passed through 0
        family = kw.get('family', 'record')
        fam = family + '_passages'
        z[fam] += 1
        rec['z0'] = z[fam]
        z['gids'] += 1
        rec['gid'] = z['gids']              # one id across every archive
        rec['fam'] = family
        rec['run'] = m['runs'] + 1          # the run this record was made in
        if CLOCKS_ON and SESSION['id'] is not None:
            rec['t'] = read_clocks(m)
        return rec
    if what == 'update':                    # a parked record changed status
        rec = kw['record']
        z['updates'] = z.get('updates', 0) + 1
        entry = [z['passages'], rec.get('status')]
        if CLOCKS_ON and SESSION['id'] is not None:
            entry.append(read_clocks(m))
        rec.setdefault('z0u', []).append(entry)
        return rec
    raise ValueError('unknown zero gate passage: ' + what)


def zero_repair(m):
    """Before saving: any record that missed the gate passes through 0 NOW.
    Nothing is refused or dropped; late passages are marked."""
    z = zero_state(m)
    total = 0
    for fam, key in (('record', 'records'), ('expression', 'expressions'), ('role', 'roles'),
                     ('node', 'nodes'), ('slot', 'slot_log'), ('product', 'products'),
                     ('division', 'divisions'), ('fraction', 'fractions'), ('unknown', 'unknowns'),
                     ('plane', 'planes'), ('view', 'views'), ('want', 'wanted'), ('punknown', 'punknowns'), ('proof', 'proofs'), ('correction', 'corrections'), ('deadlock', 'deadlocks'), ('tangent', 'tangents'), ('approach', 'approaches'), ('difference', 'differences'), ('total', 'totals')):
        missing = [r for r in m[key] if 'z0' not in r]
        if not missing:
            continue
        z[fam + '_passages'] = max([r['z0'] for r in m[key] if 'z0' in r] or [0])
        for rec in missing:
            zero_gate(m, 'record', record=rec, family=fam)
            rec['z0_late'] = True
        z['late_passages'] += len(missing)
        total += len(missing)
    return total


# ---------------- memory ----------------

def new_memory():
    return {'version': 1, 'rule': ZERO_RULE,
            'records': [],      # the counter: every S record, in order
            'expressions': [],  # every walked pair (a, b), in order
            'roles': [],        # roles the engine has found, in order
            'nodes': [],        # every S-or-turn path node, in order
            'turns': {'ptr': 0, 'roots': 0},   # next node to expand; roots made
            'slots': {},        # slot-machine state for each template
            'slot_log': [],     # every slot filling tried, in order
            'slot_cursor': [0, 0],   # diagonal over (template, filling number): [shell, template]
            'slot_parked': [],  # fillings waiting for the counter to reach a number
            'slot_refs': ['00404'],   # every template, in the order it was first seen (never reordered)
            'slot_prefs': [],   # templates made from plane points, in the order first seen
            'slot_pcursor': [0, 0],   # the same diagonal walk, for the plane templates
            'slot_ref_rec': 0,  # counter records already made into templates
            'slot_ref_pl': 0,   # plane points already looked at for templates
            'products': [],     # every repeated add and repeated turn, in order
            'mpairs': {'n': 0, 'i': 0, 'step': 0},   # where product work resumes
            'corrections': [],  # every error that was caught, who caught it, how it was fixed
            'deadlocks': [],    # every way back that ended in a move the engine blocks (a deadlock)
            'dl_cursor': {'u': 0, 'p': 0},   # how many blank searches and plane blanks were looked at for deadlocks
            'tangents': [],     # every branch off a main path, kept once
            'tg_cursor': 0,     # how many walked pairs were looked at for tangents
            'approaches': [],   # every path that closes in on a value without arriving, kept once
            'ap_cursor': 0,     # where the look at the groups of divisions resumes
            'differences': [],  # every change between two neighbouring products, kept once
            'totals': [],       # every part stacked onto the whole made so far, in order
            'pair_pause': {'sig': None},   # set when a full pass keeps no new branch: what pair exploration waits for
            'pair_base': {'n': 0, 'idx': 0},   # where the pair cursor stood when typed pairs began to be marked
            'stamp_base': {'nxt': 0, 'prod': 0, 'slot': 0},          # records below these ids were made before their changes were stamped
            'proofs': [],       # every slot filling with one number hidden and found again
            'proof_cur': [0, 0],   # next slot filling and which of its numbers to hide
            'punknowns': [],    # every blank search on the plane, in order
            'ppairs': {'n': 0, 'i': 0, 'step': 0},   # where plane blank searches resume
            'wanted': [],       # everything asked for and not found (and later found)
            'planes': [],       # every distinct point reached, in order of first reaching
            'plane_cur': 0,     # how many path nodes have been looked at for new points
            'views': [],        # every look at the plane, with its picture
            'unknowns': [],     # every blank search (a, c), in order
            'xpairs': {'n': 0, 'i': 0, 'step': 0},   # where blank searches resume
            'fractions': [],    # every leftover part, in order
            'fcursor': 0,       # how many divisions have been looked at for leftovers
            'divisions': [],    # every split-and-regroup, in order
            'dpairs': {'n': 0, 'i': 0, 'step': 0},   # where division work resumes
            'mul_parked': [],   # repeated adds waiting for the counter to grow
            'pairs': {'n': 0, 'i': 0, 'step': 0},   # where pair work resumes
            'runs': 0}


def add_record(m, value, op=None, parents=None):
    idx = len(m['records'])
    rec = {'id': idx, 'value': value, 'op': op, 'parents': parents or [], 'recipe': recipe_counter(value)}
    zero_gate(m, 'record', record=rec)
    m['records'].append(rec)
    return idx


VERIFIED = {'sig': None}     # what the archive looked like the last time it passed the replay
SAVED = {'sig': None}        # what the archive looked like when it was last written to (or read from) the main file


def archive_sig(m):
    z = zero_state(m)
    return (z['passages'], z['gids'], z.get('updates', 0), z['late_passages'], m['runs'],
            len(m['records']), len(m['wanted']), len(m['corrections']))


def verified(m):
    VERIFIED['sig'] = archive_sig(m)


# ---------------- the light check (v23.12) ----------------
# The full replay re-solves every blank search and product from S. That is most of the time. It runs once, at
# start-up. After that the engine remembers a fingerprint of every record in those three families. Before a save,
# the replay skips ONLY the records whose fingerprint is unchanged since they were re-solved this launch; anything new
# or changed is re-solved from S, and every other check runs in full. If this check fails, the full replay decides.

REPLAY_SKIP = {'unknowns': frozenset(), 'products': frozenset(), 'punknowns': frozenset()}   # empty = nothing skipped = full replay
SNAP = {'obj': None, 'h': {}}


def rec_print(r):
    return hashlib.blake2b(json.dumps(r, sort_keys=True, separators=(',', ':')).encode('utf-8'), digest_size=8).digest()


def take_snapshot(m):
    """Called only right after a FULL replay (or a passing light check): remembers what was just checked."""
    SNAP['obj'] = m
    SNAP['h'] = {f: [rec_print(r) for r in m[f]] for f in REPLAY_SKIP}


def replay_light(m):
    """The check before saving. Same verdict as the full replay, much faster after the first run of a launch."""
    if SNAP['obj'] is not m:
        return replay(m)                     # nothing was checked from 0 for this archive yet: do the full one
    skip = {}
    for f in REPLAY_SKIP:
        old, cur = SNAP['h'][f], m[f]
        if len(cur) < len(old):
            return replay(m)                 # a family got shorter: not normal, so the full replay decides
        skip[f] = frozenset(i for i in range(len(old)) if rec_print(cur[i]) == old[i])
    held = GATE['m']
    flush_inner()
    GATE['m'] = None
    REPLAY_SKIP.update(skip)
    try:
        problems = _replay_plain(m)
    finally:
        REPLAY_SKIP.update({f: frozenset() for f in REPLAY_SKIP})
        GATE['m'] = held
    if problems:
        return replay(m)                     # a failure is always confirmed by the full replay
    take_snapshot(m)
    return problems


CACHE_OWNER = {}     # cache name -> (the archive list it was built from, its length then)


def cache_fresh(name, listing):
    owner = CACHE_OWNER.get(name)
    return owner is not None and owner[0] is listing and owner[1] == len(listing)


def cache_stamp(name, listing):
    CACHE_OWNER[name] = (listing, len(listing))


def clear_caches():
    CACHE_OWNER.clear()
    NODE_INDEX.clear()
    PLANE_SEEN.clear()
    WANT_SEEN.clear()
    DIV_SEEN.clear()


def shape_problems(data):
    """Is this a whole archive? Every part present and of the right kind, every archive a list of records."""
    if not isinstance(data, dict):
        return ['the file does not hold an archive']
    out = []
    for key, val in new_memory().items():
        if key not in data:
            out.append('missing part: %s' % key)
        elif type(data[key]) is not type(val):
            out.append('%s is the wrong kind of thing' % key)
    if not out:
        for fam, key in FAMILIES:
            if not all(isinstance(r, dict) for r in data[key]):
                out.append('%s holds something that is not a record' % key)
    return out


def read_archive(path):
    """A compressed file or a plain JSON one, told apart by the first two bytes."""
    with open(path, 'rb') as f:
        raw = f.read()
    if raw[:2] == b'\x1f\x8b':
        raw = gzip.decompress(raw)
    return json.loads(raw.decode('utf-8'))


def open_candidate(path):
    """Read one file and check it from 0. Returns (archive, None) or (None, why it was refused)."""
    try:
        m = read_archive(path)
    except (ValueError, OSError, EOFError, zlib.error) as exc:
        return None, 'could not be read (%s)' % exc.__class__.__name__
    upgrade_pairs(m)
    upgrade_stamps(m)
    if upgrade_totals(m):
        print('  %s is from before the totals library: the empty library was added. It fills in over the next runs.' % os.path.basename(path))
    if upgrade_differences(m):
        print('  %s is from before the differences library: the empty library was added. It fills in over the next runs.' % os.path.basename(path))
    if upgrade_approaches(m):
        print('  %s is from before the approaches library: the empty library was added. It fills in over the next runs.' % os.path.basename(path))
    if upgrade_tangents(m):
        print('  %s is from before the tangent library: the empty library was added. It fills in over the next runs.' % os.path.basename(path))
    if upgrade_old(m):
        print('  %s is from before the deadlock library: the empty library was added. It fills in over the next runs.' % os.path.basename(path))
    bad = shape_problems(m)
    if bad:
        return None, 'is not a whole archive: ' + '; '.join(bad[:3])
    try:
        clear_caches()
        start_session(m)
        if not m['records']:
            return None, 'holds no counter'
        seed_corrections(m)
        if upgrade_credits(m):
            print('  %s: older correction labels were changed to the Dragon Z version names, each as a Z0 stamp.' % os.path.basename(path))
        start_turns(m)
        build_index(m)
        upgrade_watch(m)
        if group_role(m):
            print('  %s: the role group was written down from the first stack it already holds (a stamped record).' % os.path.basename(path))
        if difference_role(m):
            print('  %s: the role difference was written down from the first change it already holds (a stamped record).' % os.path.basename(path))
        if limit_role(m):
            print('  %s: the role limit was written down from the first approach it already holds (a stamped record).' % os.path.basename(path))
        problems = replay(m)
    except Exception as exc:                 # a damaged file gives a reason, never a crash
        return None, 'could not be checked (%s: %s)' % (exc.__class__.__name__, exc)
    if problems:
        return None, 'fails the replay: ' + '; '.join(problems[:3])
    verified(m)
    take_snapshot(m)
    return m, None


def keep_aside(path):
    """A refused file is kept under its own name. Nothing is deleted or written over."""
    stamp = time.strftime('%Y%m%d-%H%M%S')
    new = '%s.refused-%s' % (path, stamp)
    n = 0
    while os.path.exists(new):
        n += 1
        new = '%s.refused-%s-%d' % (path, stamp, n)
    os.replace(path, new)
    return new


def load_memory():
    path = memory_path()
    src = path                                # the file this launch reads
    if not os.path.exists(path) and not os.path.exists(path + '.bak'):
        old = legacy_path()
        if os.path.exists(old) or os.path.exists(old + '.bak'):
            src = old
    have_main, have_bak = os.path.exists(src), os.path.exists(src + '.bak')
    if not have_main and not have_bak:
        clear_caches()
        m = new_memory()
        start_session(m)
        add_record(m, 0, op='Z0')            # Z0 itself: zero is the first record, and it goes through the gate
        seed_corrections(m)
        start_turns(m)
        build_index(m)
        verified(m)
        return m
    m = None
    for p in (src, src + '.bak'):
        if not os.path.exists(p):
            continue
        m, why = open_candidate(p)
        if m is not None:
            if p == src:
                if src == path:
                    SAVED['sig'] = archive_sig(m)
                else:
                    print('  Read from the plain file of the earlier versions. The first save writes the compressed file and leaves the plain one as it is.')
                print('Archive checked from 0 before anything else: it passes.')
            else:
                print('The backup passes the check and is being used.')
                if have_main:
                    print('  The main file was kept under another name: %s' % os.path.basename(keep_aside(src)))
            break
        print('  %s %s' % (os.path.basename(p), why))
    if m is None:
        print('Neither saved file passes the check, so nothing was loaded and nothing was changed on disk.')
        print('Both files are still exactly as they were. Look at them, or move them, before running again.')
    return m


def export_plain(m):
    """A readable copy for looking at or sharing. The engine never reads it back."""
    path = export_path()
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(m, f, separators=(',', ':'))
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)
    return path, os.path.getsize(path)


def save_memory(m):
    """Saves only an archive that passes the replay. A failing archive leaves the files on disk untouched."""
    zero_repair(m)
    if archive_sig(m) == SAVED['sig'] and os.path.exists(memory_path()):
        return True                          # nothing changed since the last write: the previous backup stays the previous one
    if archive_sig(m) != VERIFIED['sig']:
        problems = replay_light(m)
        if problems:
            print('NOT SAVED: the archive fails its own replay, so the files on disk were left exactly as they were.')
            for p in problems[:5]:
                print('    -', p)
            return False
        verified(m)
    path = memory_path()
    tmp = path + '.tmp'
    blob = gzip.compress(json.dumps(m, separators=(',', ':')).encode('utf-8'), GZIP_LEVEL)
    with open(tmp, 'wb') as f:
        f.write(blob)
        f.flush()
        os.fsync(f.fileno())
    if BACKUP_ON_SAVE and os.path.exists(path):
        os.replace(path, path + '.bak')
    os.replace(tmp, path)
    SAVED['sig'] = archive_sig(m)
    return True


# ---------------- the work ----------------

def step(m):
    """One S step: newest value -> next value. Both the step and the record
    go through Z0. The newest record keeps a link to its S successor."""
    last = m['records'][-1]
    nxt = zero_gate(m, 'operation', name='S', args=(last['value'],))
    new = add_record(m, nxt, op='S', parents=[last['id']])
    last['nxt'] = new


def next_pair(m, key='pairs', size=None):
    """Walk every pair (n, i) with i <= n, both orders. Resumes where it stopped."""
    c = m[key]
    while True:
        n, i, s = c['n'], c['i'], c['step']
        if n >= (len(m['records']) if size is None else size):
            return None
        limit = 1 if i == n else 2
        if s < limit:
            break
        c.update(n=n + (i >= n), i=0 if i >= n else i + 1, step=0)
    c['step'] = s + 1
    return (n, i) if s == 0 else (i, n)


def find_role(m, name):
    for r in m['roles']:
        if r['name'] == name:
            return r
    return None


# ---------------- 00404 SLOT MACHINE ----------------

def breakdown(text):
    """A digit c becomes c units of 1. A 0 stays a 0. An i stays an i (a turn marker)."""
    return ''.join('0' if ch == '0' else ch if ch == 'i' else '1' * int(ch) for ch in text)


def slot_refs(m):
    """00404 first, then every counted number, then every plane point with an i part (3+2i is 3i2).
    New templates are only ever added at the end."""
    refs = m['slot_refs']
    have = set(refs)
    for r in m['records'][m['slot_ref_rec']:]:
        ref = str(r['value'])
        if ref not in have:
            refs.append(ref)
            have.add(ref)
    m['slot_ref_rec'] = len(m['records'])
    prefs = m['slot_prefs']
    have |= set(prefs)
    for p in m['planes'][m['slot_ref_pl']:]:
        if p['p'][1] != 0:
            ref = '%di%d' % (abs(p['p'][0]), abs(p['p'][1]))
            if ref not in have:
                prefs.append(ref)
                have.add(ref)
    m['slot_ref_pl'] = len(m['planes'])
    return refs, prefs


def slot_state(m, ref):
    key = ref + '|' + SLOT_SIG
    if key not in m['slots']:
        symbols = breakdown(ref)
        m['slots'][key] = {'ref': ref, 'symbols': symbols, 'next': 0,
                           'total': len(SLOT_OPS) ** (len(symbols) - 1)}
    return m['slots'][key]


def slot_filling(symbols, n):
    """Filling number n -> one choice per slot (the first slot changes slowest)."""
    k, slots = len(SLOT_OPS), len(symbols) - 1
    choice = []
    for _ in range(slots):
        n, digit = divmod(n, k)
        choice.append(SLOT_OPS[digit])
    return choice[::-1]


def slot_groups(symbols, choice):
    """Split the symbols at every operation slot. Joined symbols make one group of digits and i marks."""
    groups, ops, digits = [], [], symbols[0]
    for op, sym in zip(choice, symbols[1:]):
        if op == 'join':
            digits += sym
        else:
            groups.append(digits)
            ops.append(op)
            digits = sym
    groups.append(digits)
    return groups, ops


@lru_cache(maxsize=200000)
def group_value(num, limit):
    """Count a joined group of 0 and 1 symbols. Each symbol: the number so far is added to itself ten
    times (the repeat of adding that multiply was found from), then a 1 takes one S step.
    None if the counter has not reached it."""
    acc = 0
    for ch in num:
        acc = repeat_add(acc, 10, limit)
        if acc is None:
            return None
        if ch == '1':
            acc = S(acc)
        if acc >= limit:
            return None
    return acc


@lru_cache(maxsize=200000)
def group_point(digits, limit):
    """11i is 11 turned once. i alone is i. Every i mark is one literal turn of the units.
    The point as (real, i), or None if the counter has not reached the number."""
    num = digits.replace('i', '')
    n = group_value(num, limit) if num else S(0)
    if n is None:
        return None
    c = [n, 0, 0, 0]
    for _ in range(digits.count('i')):
        c = turn_units(c)
    return (c[0] - c[2], c[1] - c[3])


def slot_numbers(symbols, choice, limit, count=None):
    """The points of every group. A group the counter has not reached (at this limit) is None."""
    groups, ops = slot_groups(symbols, choice)
    count = count or group_point
    return [count(g, limit) for g in groups], ops


def slot_need(nums, limit):
    """How far the counter must reach. Uncountable at this limit means: past this limit."""
    if any(p is None for p in nums):
        return limit
    return max(max(abs(p[0]), abs(p[1])) for p in nums)


def slot_text(symbols, choice):
    out = symbols[0]
    for op, sym in zip(choice, symbols[1:]):
        out += ('' if op == 'join' else op) + sym
    return out


def evaluate_slot(nums, ops, binop):
    """Usual order: * / T first (left to right), then + and - left to right.
    binop(op, a, b) works on (real, i, denominator). Returns a triple, None if something does
    not fit in the counter yet, or one of BLOCKS."""
    vals, rest = [(nums[0][0], nums[0][1], 1)], []
    for op, n in zip(ops, nums[1:]):
        if op in '*/T':
            r = binop(op, vals[-1], (n[0], n[1], 1))
            if r is None or r in BLOCKS:
                return r
            vals[-1] = r
        else:
            rest.append(op)
            vals.append((n[0], n[1], 1))
    acc = vals[0]
    for op, v in zip(rest, vals[1:]):
        acc = binop(op, acc, v)
        if acc is None or acc in BLOCKS:
            return acc
    return acc


def compute_slot(m, nums, ops, limit):
    return evaluate_slot(
        nums, ops,
        lambda op, a, b: zero_gate(m, 'operation', name='slotop', args=(op, a, b, limit)))


def settle_slot(rec, res):
    """Write the outcome of a filling onto its record. Returns True if it is settled."""
    if isinstance(res, str):
        rec['value'], rec['im'], rec['den'], rec['status'], rec['why'] = None, None, None, 'blocked', res
        return True
    if res is not None:
        rec['value'], rec['im'], rec['den'], rec['status'] = res[0], res[1], res[2], 'done'
        rec.pop('why', None)
        return True
    return False


def do_slot(m, ref, n):
    st = slot_state(m, ref)
    choice = slot_filling(st['symbols'], n)
    limit = len(m['records'])
    nums, ops = slot_numbers(st['symbols'], choice, limit,
                             lambda g, lim: zero_gate(m, 'operation', name='group', args=(g, lim)))
    # The engine's own progress is the limit: a number can only be used once the
    # counter has reached it. Until then the filling is PARKED, kept and retried.
    need = slot_need(nums, limit)
    rec = {'id': len(m['slot_log']), 'ref': ref, 'n': n, 'text': slot_text(st['symbols'], choice),
           'used': len(ops), 'need': need, 'limit': limit, 'value': None, 'im': None, 'den': None, 'status': 'parked'}
    rec['recipe'] = recipe_slot(m, rec)
    if need < limit:
        settle_slot(rec, compute_slot(m, nums, ops, limit))
    zero_gate(m, 'record', record=rec, family='slot')
    m['slot_log'].append(rec)
    if rec['status'] == 'parked':
        m['slot_parked'].append(rec['id'])
    st['next'] = n + 1
    return rec


def retry_slots(m):
    """Parked fillings get another go when the counter has grown past what blocked them."""
    if slots_waiting(m):
        return 0
    still, freed = [], 0
    for rid in m['slot_parked']:
        rec = m['slot_log'][rid]
        if rec['need'] < len(m['records']) and len(m['records']) > rec['limit']:
            st = slot_state(m, rec['ref'])
            rec['limit'] = len(m['records'])
            nums, ops = slot_numbers(st['symbols'], slot_filling(st['symbols'], rec['n']), rec['limit'],
                                     lambda g, lim: zero_gate(m, 'operation', name='group', args=(g, lim)))
            rec['need'] = slot_need(nums, rec['limit'])
            if rec['need'] >= rec['limit']:
                still.append(rid)
                continue
            if settle_slot(rec, compute_slot(m, nums, ops, rec['limit'])):
                zero_gate(m, 'update', record=rec)
                freed += 1
                continue
        still.append(rid)
    m['slot_parked'] = still
    return freed


def slots_waiting(m):
    return [name for name, _ in OP_ROLES if find_role(m, name) is None] + \
           (['fraction'] if find_role(m, 'fraction') is None else [])


def dovetail(m, refs, c, budget):
    done = skipped = 0
    while done < budget and skipped < 2 * len(refs) + 10 and not STOP['flag']:
        shell, i = c
        if i > shell or i >= len(refs):
            c[0], c[1] = shell + 1, 0
            continue
        n = shell - i
        st = slot_state(m, refs[i])
        c[1] = i + 1
        if st['next'] > n or st['next'] >= st['total']:      # not its turn yet, or all its fillings are done
            skipped += 1
            continue
        skipped = 0
        do_slot(m, refs[i], st['next'])      # its own next filling, even if it started late
        done += 1
    return done


def run_slots(m, budget):
    """Dovetail over (template, filling): shell s tries filling s-i of template i for every i.
    00404 and the counted numbers share the budget with the plane-point templates, half each."""
    waiting = slots_waiting(m)
    if waiting:
        return 0, waiting
    refs, prefs = slot_refs(m)
    first = dovetail(m, refs, m['slot_cursor'], budget - budget // 2 if prefs else budget)
    second = dovetail(m, prefs, m['slot_pcursor'], budget // 2) if prefs else 0
    return first + second, []


def slot_value_text(r):
    if r['im']:
        return value_text((r['value'], r['im']))
    return str(r['value']) if r['den'] == 1 else mixed('-' if r['value'] < 0 else '', 0, abs(r['value']), r['den'])


def slot_line(m, r):
    if r['status'] == 'parked':
        return '#%d  %s = ?   (template %s, filling %d) parked: waits for the counter to grow' % (
            r['id'], r['text'], r['ref'], r['n'])
    if r['status'] == 'blocked':
        return '#%d  %s = blocked   (template %s, filling %d) %s; kept\n         recipe: %s' % (
            r['id'], r['text'], r['ref'], r['n'], BLOCK_WHY[r['why']], recipe_slot(m, r))
    where = ''
    if r['im']:
        pid = plane_seen(m).get((r['value'], r['im']))
        where = '   on the plane: %s, %s' % (plane_place((r['value'], r['im'])),
                                             'reached by the paths (point #%d)' % pid if pid is not None else 'not reached by the paths yet')
    return '#%d  %s = %s   (template %s, filling %d, %d operation%s used)%s\n         recipe: %s' % (
        r['id'], r['text'], slot_value_text(r), r['ref'], r['n'], r['used'], '' if r['used'] == 1 else 's',
        where, recipe_slot(m, r))


def show_slots(m, n=10):
    print('\n00404 SLOT MACHINE')
    waiting = slots_waiting(m)
    if waiting:
        print('  Waiting for these to be found first:', ' '.join(waiting))
    st = slot_state(m, SLOT_TEMPLATE)
    print('  %s -> %s | %d slots | each slot: %s | filling %d of %d tried'
          % (SLOT_TEMPLATE, st['symbols'], len(st['symbols']) - 1, ' '.join(SLOT_OPS), st['next'], st['total']))
    log = m['slot_log']
    done = [r for r in log if r['status'] == 'done']
    zeros = sum(1 for r in done if r['value'] == 0 and not r['im'])
    negs = sum(1 for r in done if r['value'] < 0 and not r['im'])
    fracs = sum(1 for r in done if r['den'] > 1)
    pts = [r for r in done if r['im']]
    blocked = sum(1 for r in log if r['status'] == 'blocked')
    print('  Fillings tried: %d | done: %d | blocked: %d | parked (counter has not reached their numbers yet): %d'
          % (len(log), len(done), blocked, len(m['slot_parked'])))
    print('  Across %d templates (%d from plane points) | results of zero: %d | negative: %d | fractions: %d | distinct values: %d'
          % (len(set(r['ref'] for r in log)), len(set(r['ref'] for r in log if 'i' in r['ref'])), zeros, negs, fracs,
             len(set((r['value'], r['im'], r['den']) for r in done))))
    print('  Landed on the plane (an i part): %d fillings, %d distinct points, %d of those not reached by the paths yet'
          % (len(pts), len(set((r['value'], r['im']) for r in pts)),
             len(set((r['value'], r['im']) for r in pts if (r['value'], r['im']) not in plane_seen(m)))))
    for r in log[-n:]:
        print('  ' + slot_line(m, r))


# ---------------- the i turn: paths of S steps and turns ----------------

NODE_INDEX = {}      # value (real, imaginary) -> node ids. Rebuilt on load.


def node_value(c):
    return (c[0] - c[2], c[1] - c[3])


def value_text(v):
    re_, im = v
    if im == 0:
        return str(re_)
    imt = 'i' if abs(im) == 1 else '%di' % abs(im)
    if re_ == 0:
        return ('-' if im < 0 else '') + imt
    return '%d%s%s' % (re_, '-' if im < 0 else '+', imt)


def build_index(m):
    NODE_INDEX.clear()
    for n in m['nodes']:
        NODE_INDEX.setdefault(node_value(n['c']), []).append(n['id'])


# Roles the engine finds for itself. Each is written down the first time a path
# node shows it. The test is only a description of what was seen.
TURN_ROLES = (
    ('half_turn', lambda n: n['tr'] == 2, 'two turns in a row: facing the opposite way'),
    ('right_turn', lambda n: n['tr'] == 3, 'three turns in a row: the other way round from one turn'),
    ('full_turn', lambda n: n['tr'] == 4 and n['d'] == 0, 'four turns in a row: back where it started, so the turns cancel back to Z0'),
    ('subtract', lambda n: n['cx'], 'an S step met its opposite unit; both went back to Z0'),
    ('negative', lambda n: n['c'][0] - n['c'][2] < 0, 'a path holds less than nothing on the real line'),
    ('imaginary', lambda n: n['c'][1] > 0 or n['c'][3] > 0, 'a path holds units turned toward i'),
    ('minus_i', lambda n: n['c'][1] - n['c'][3] < 0, 'a path holds -i'),
)


def add_role(m, name, rule, **extra):
    role = {'id': len(m['roles']), 'name': name, 'rule': rule}
    role.update(extra)
    zero_gate(m, 'record', record=role, family='role')
    m['roles'].append(role)
    return role


def add_node(m, act, parent, origin, c, d, cx, tr=0):
    node = {'id': len(m['nodes']), 'a': act, 'p': parent, 'o': origin, 'c': list(c), 'd': d, 'cx': bool(cx), 'tr': tr}
    zero_gate(m, 'record', record=node, family='node')
    m['nodes'].append(node)
    node['recipe'] = recipe_node(m, node['id'])
    NODE_INDEX.setdefault(node_value(node['c']), []).append(node['id'])
    for name, test, why in TURN_ROLES:
        if find_role(m, name) is None and test(node):
            add_role(m, name, TURN_ROLE_RULE, kind='node', evidence=node['id'], why=why,
                     recipe=recipe_node(m, node['id']))
    return node


def add_root(m):
    """A counter record starts a path: k units of +1, facing +1."""
    k = m['turns']['roots']
    add_node(m, 'root', None, k, [m['records'][k]['value'], 0, 0, 0], 0, False)
    m['turns']['roots'] = k + 1


def start_turns(m):
    if find_role(m, 'i') is None:
        add_role(m, 'i', I_ACTION_RULE, kind='given', given=True, recipe='I')
    if find_role(m, SLOT_TEMPLATE) is None:
        add_role(m, SLOT_TEMPLATE, SLOT_RULE, kind='given', given=True)
    if not m['nodes']:
        add_root(m)


def expand(m):
    """Take the next node and explore both of its futures: an S step and an i turn."""
    ptr = m['turns']['ptr']
    p = m['nodes'][ptr]
    c, cx = zero_gate(m, 'operation', name='Sd', args=(p['c'], p['d']))
    add_node(m, 'S', ptr, p['o'], c, p['d'], cx, 0)
    d2 = zero_gate(m, 'operation', name='I', args=(p['d'],))
    add_node(m, 'I', ptr, p['o'], p['c'], d2, False, p['tr'] + 1)
    m['turns']['ptr'] = ptr + 1
    if m['turns']['roots'] < len(m['records']):     # a new path may start at any counted number
        add_root(m)


def node_word(m, nid):
    acts = []
    n = m['nodes'][nid]
    while n['a'] != 'root':
        acts.append(n['a'])
        if len(acts) > len(m['nodes']):
            return n['o'], '(this path loops back on itself: the archive is damaged)'
        n = m['nodes'][n['p']]
    return n['o'], ' '.join(reversed(acts)) or '(nothing)'


# ---------------- RECIPES: the S steps and i turns behind everything ----------------

def rle(acts):
    out = []
    for a in acts:
        if out and out[-1][0] == a:
            out[-1][1] += 1
        else:
            out.append([a, 1])
    return ' '.join(a if n == 1 else '%s*%d' % (a, n) for a, n in out)


def recipe_counter(n):
    return 'S*%d' % n


def recipe_add(a, b):
    return 'S*%d S*%d' % (a, b)                 # get to a, then take b more S steps


def recipe_multiply(a, b):
    return '[S*%d]x%d' % (a, b)                 # add a again and again, b times


def recipe_rotate(a, b):
    return 'S*%d T*%d' % (a, b)                 # get to a, then turn every unit b times


def recipe_divide(a, b):
    return 'S*%d R*%d' % (a, b)                 # get to a, then split it into groups of b


def recipe_fraction(a, b, g):
    """Get to a, split into groups of b, take the leftover as a part of a group (F),
    and if it can be written in fewer parts, split part and group by g (G)."""
    return 'S*%d R*%d F' % (a, b) + (' G*%d' % g if g >= 2 else '')


def layout_text(q, b, rem):
    """How the units sit after the split: 1*4 is four units, 0 is a split."""
    if q == 0 and rem == 0:
        return '(nothing)'
    if q == 0:
        text = '1*%d' % rem
        return text
    text = '1*%d' % b if q == 1 else '[1*%d 0]x%d 1*%d' % (b, q - 1, b)
    return text + (' 0 1*%d' % rem if rem else '')


def recipe_node(m, nid):
    origin, word = node_word(m, nid)
    txt = rle([] if word == '(nothing)' else word.split())
    return 'S*%d' % origin + (' ' + txt if txt else '')


def recipe_group(digits):
    k = digits.count('i')
    num = digits.replace('i', '').lstrip('0') or ('0' if digits.replace('i', '') else '1')
    return 'S*' + num + (' T*%d' % k if k else '')


def recipe_slot(m, rec):
    st = slot_state(m, rec['ref'])
    groups, ops = slot_groups(st['symbols'], slot_filling(st['symbols'], rec['n']))
    vals, rest = [recipe_group(groups[0])], []
    for op, g in zip(ops, groups[1:]):
        plain = 'i' not in g
        n = (g.lstrip('0') or '0') if plain else None
        if op == '*':
            vals[-1] = '[%s]x%s' % (vals[-1], n) if plain else '[%s]x(%s)' % (vals[-1], recipe_group(g))
        elif op == '/':
            vals[-1] = '[%s]R*%s' % (vals[-1], n) if plain else '[%s]R*(%s)' % (vals[-1], recipe_group(g))
        elif op == 'T':
            vals[-1] = '[%s]T*%s' % (vals[-1], n) if plain else '[%s]T*(%s)' % (vals[-1], recipe_group(g))
        else:
            rest.append(op)
            vals.append(recipe_group(g))
    out = [vals[0]]
    for op, v in zip(rest, vals[1:]):
        out.append(v if op == '+' else 'I*2 %s I*2' % v)    # take away: face -1, step, face +1 again
    return ' '.join(out)


def role_recipe(m, r):
    """The recipe a role should carry, worked out again from the record it points at."""
    recs = m['records']
    if r['name'] == 'i':
        return 'I'
    if r.get('kind') == 'node':
        return recipe_node(m, r['evidence'])
    if r['name'] == 'add':
        e = m['expressions'][r['evidence']]
        return recipe_add(recs[e['l']]['value'], recs[e['r']]['value'])
    if r.get('kind') == 'product':
        p = m['products'][r['evidence']]
        a, b = recs[p['l']]['value'], recs[p['r']]['value']
        return recipe_multiply(a, b) if p['kind'] == 'multiply' else recipe_rotate(a, b)
    if r.get('kind') == 'division':
        d = m['divisions'][r['evidence']]
        return recipe_divide(recs[d['l']]['value'], recs[d['r']]['value'])
    if r.get('kind') == 'proof':
        p = m['proofs'][r['evidence']]
        return recipe_proof(m, m['slot_log'][p['slot']], p['g'])
    if r.get('kind') == 'punknown':
        u = m['punknowns'][r['evidence']]
        f = u['forms'][r['form']]
        return recipe_punknown(m, f['op'], f['side'], tuple(m['planes'][u['l']]['p']), tuple(m['planes'][u['r']]['p']),
                               punknown_role_x(r['name'], f))
    if r.get('kind') == 'plane':
        return recipe_node(m, m['planes'][r['evidence']]['node'])
    if r.get('kind') == 'unknown':
        u = m['unknowns'][r['evidence']]
        f = u['forms'][r['form']]
        return recipe_unknown(f['op'], f['side'], recs[u['l']]['value'], recs[u['r']]['value'],
                              unknown_role_x(r['name'], f))
    if r.get('kind') == 'approach':
        return approach_recipe(m, m['approaches'][r['evidence']])
    if r.get('kind') == 'difference':
        return difference_recipe(m, m['differences'][r['evidence']])
    if r.get('kind') == 'total':
        return total_recipe(m, m['totals'][r['evidence']])
    if r.get('kind') == 'fraction':
        f = m['fractions'][r['evidence']]
        d = m['divisions'][f['div']]
        return recipe_fraction(recs[d['l']]['value'], recs[d['r']]['value'], f['g'])
    return None


def replay_recipes(m):
    problems = []
    for r in m['roles']:
        try:
            want = role_recipe(m, r)
        except (TypeError, KeyError, IndexError, ValueError):
            problems.append('role %s points at a record that does not show it' % r['name'])
            continue
        if want is None:
            if 'recipe' in r:
                problems.append('role %s carries a recipe it should not have' % r['name'])
        elif r.get('recipe') != want:
            problems.append('role %s: its recipe %r should be %r' % (r['name'], r.get('recipe'), want))
    return problems


FAMILIES = (('record', 'records'), ('expression', 'expressions'), ('role', 'roles'),
            ('node', 'nodes'), ('slot', 'slot_log'), ('product', 'products'),
            ('division', 'divisions'), ('fraction', 'fractions'), ('unknown', 'unknowns'),
            ('plane', 'planes'), ('view', 'views'), ('want', 'wanted'), ('punknown', 'punknowns'), ('proof', 'proofs'), ('correction', 'corrections'), ('deadlock', 'deadlocks'), ('tangent', 'tangents'), ('approach', 'approaches'), ('difference', 'differences'), ('total', 'totals'))


def expected_recipe(m, fam, r):
    recs = m['records']
    if fam == 'record':
        return recipe_counter(r['value'])
    if fam == 'expression':
        return recipe_add(recs[r['l']]['value'], recs[r['r']]['value'])
    if fam == 'product':
        a, b = recs[r['l']]['value'], recs[r['r']]['value']
        return recipe_multiply(a, b) if r['kind'] == 'multiply' else recipe_rotate(a, b)
    if fam == 'division':
        return recipe_divide(recs[r['l']]['value'], recs[r['r']]['value'])
    if fam == 'fraction':
        d = m['divisions'][r['div']]
        return recipe_fraction(recs[d['l']]['value'], recs[d['r']]['value'], r['g'])
    if fam == 'unknown':
        return recipe_unknown_pair(recs[r['l']]['value'], recs[r['r']]['value'])
    if fam == 'correction':
        return correction_recipe(r['what'])
    if fam == 'deadlock':
        return deadlock_recipe(m, r)
    if fam == 'tangent':
        return tangent_recipe(r['kind'], r['p'])
    if fam == 'approach':
        return approach_recipe(m, r)
    if fam == 'difference':
        return difference_recipe(m, r)
    if fam == 'total':
        return total_recipe(m, r)
    if fam == 'proof':
        return recipe_proof(m, m['slot_log'][r['slot']], r['g'])
    if fam == 'punknown':
        return recipe_punknown_pair(m, r['l'], r['r'])
    if fam == 'want':
        return recipe_wanted(tuple(r['key']))
    if fam == 'plane':
        return recipe_node(m, r['node'])
    if fam == 'view':
        return 'S*%d I*2 S*%d' % (r['r'], r['r'])
    if fam == 'node':
        return recipe_node(m, r['id'])
    if fam == 'slot':
        return recipe_slot(m, r)
    return role_recipe(m, r)


def replay_identity(m):
    """Every record carries its id stamps and the recipe it should have."""
    problems = []
    z = zero_state(m)
    seen = set()
    for fam, key in FAMILIES:
        for r in m[key]:
            gid = r.get('gid')
            if gid is None or r.get('fam') != fam or not isinstance(r.get('run'), int) or r['run'] > m['runs'] + 1:
                problems.append('%s record %s is missing its global id, family or run' % (fam, r.get('id')))
            elif gid in seen or not 1 <= gid <= z['gids']:
                problems.append('global id %d is used twice or out of range' % gid)
            else:
                seen.add(gid)
            if CLOCKS_ON and 't' not in r and 'z0_late' not in r:
                problems.append('%s record %s has no clock stamp' % (fam, r.get('id')))
            if fam != 'role' and r.get('recipe') != expected_recipe(m, fam, r):
                problems.append('%s record %s: its recipe %r should be %r'
                                % (fam, r.get('id'), r.get('recipe'), expected_recipe(m, fam, r)))
            if len(problems) >= 20:
                problems.append('... more problems not listed')
                return problems
    if len(seen) != z['gids'] and not problems:
        problems.append('%d global ids were handed out but %d records carry one' % (z['gids'], len(seen)))
    return problems


def find_gid(m, gid):
    for fam, key in FAMILIES:
        for r in m[key]:
            if r.get('gid') == gid:
                return fam, r
    return None, None


def identity_lines(fam, r):
    out = ['  global id %s | %s #%s | made in run %s | Z0 passage %s of its archive'
           % (r.get('gid'), fam, r.get('id'), r.get('run'), r.get('z0'))]
    if 't' in r:
        out.append('  made at ' + clock_line(r['t']))
    if r.get('recipe'):
        out.append('  recipe: ' + r['recipe'])
    if r.get('z0u'):
        out.append('  changed %d time(s) after it was made, each stamped through Z0' % len(r['z0u']))
    return out


def recipes_report(m):
    print('  S = one S step | I = one i turn | T = one i turn of every unit | [..]xN = repeat N times')
    print('  R*b = split into groups of b with a 0 between each (units 1*4 0 1*4)')
    print('  F = the leftover units are a part of a group | G*g = split part and group by g')
    print('  S*0 = no steps taken: it stayed at Z0')
    print('  D = a way back that ended in a move the engine blocks: a deadlock')
    print('  T = a branch off a main path: S*p I S is a turn then a step, S*p I*2 S is a step back')
    for r in m['roles']:
        if 'recipe' in r:
            print('  %-10s %s' % (r['name'], r['recipe']))
        else:
            print('  %-10s (given: not made from S and i)' % r['name'])


# ---------------- multiplication: repeating the actions already found ----------------

def product_role(m, name, rid, base, count):
    if find_role(m, name) is None:
        why = {'multiply': 'adding a again and again, b times, from nothing',
               'rotate': 'turning every unit of a, b times, changed the number'}[name]
        add_role(m, name, MUL_ROLE_RULE, kind='product', evidence=rid, why=why,
                 recipe=recipe_multiply(base, count) if name == 'multiply' else recipe_rotate(base, count))


def do_product(m, a, b, manual=False):
    """One pair gives two records: repeat the add, and repeat the turn."""
    base, count = m['records'][a]['value'], m['records'][b]['value']
    limit = len(m['records'])
    r = zero_gate(m, 'operation', name='repeat_add', args=(base, count, limit))
    rid = len(m['products'])
    if r is not None and count >= 2:
        product_role(m, 'multiply', rid, base, count)
    rec = {'id': rid, 'kind': 'multiply', 'l': a, 'r': b, 'limit': limit, 'tries': 1,
           'op': 'multiply' if find_role(m, 'multiply') else 'repeat_add',
           'v': None if r is None else [r, 0], 'status': 'parked' if r is None else 'done',
           'recipe': recipe_multiply(base, count)}
    if manual:
        rec['manual'] = True      # asked for by hand, so it sits outside the pair order
    zero_gate(m, 'record', record=rec, family='product')
    m['products'].append(rec)
    if r is None:
        m['mul_parked'].append(rid)
    v = zero_gate(m, 'operation', name='repeat_turn', args=(base, count))
    rid = len(m['products'])
    if v != [base, 0]:
        product_role(m, 'rotate', rid, base, count)
    rec = {'id': rid, 'kind': 'rotate', 'l': a, 'r': b, 'v': v, 'status': 'done',
           'op': 'rotate' if find_role(m, 'rotate') else 'repeat_turn',
           'recipe': recipe_rotate(base, count)}
    if manual:
        rec['manual'] = True
    zero_gate(m, 'record', record=rec, family='product')
    m['products'].append(rec)


def retry_products(m):
    """Repeated adds that did not fit in the counter get another go when it has grown."""
    still, freed = [], 0
    for rid in m['mul_parked']:
        rec = m['products'][rid]
        if len(m['records']) > rec['limit']:
            base, count = m['records'][rec['l']]['value'], m['records'][rec['r']]['value']
            rec['limit'] = len(m['records'])
            rec['tries'] += 1
            r = zero_gate(m, 'operation', name='repeat_add', args=(base, count, rec['limit']))
            if r is not None:
                rec['v'], rec['status'] = [r, 0], 'done'
                if count >= 2:
                    product_role(m, 'multiply', rid, base, count)
                if find_role(m, 'multiply'):
                    rec['op'] = 'multiply'
                zero_gate(m, 'update', record=rec)
                freed += 1
                continue
        still.append(rid)
    m['mul_parked'] = still
    return freed


def product_line(m, p):
    a, b = m['records'][p['l']]['value'], m['records'][p['r']]['value']
    rc = recipe_multiply(a, b) if p['kind'] == 'multiply' else recipe_rotate(a, b)
    if p['kind'] == 'multiply':
        if p['status'] == 'parked':
            return '#%d  %d x %d = ?   (add %d, %d times) parked: the counter has not reached the answer' % (p['id'], a, b, a, b)
        return '#%d  %d x %d = %d   (add %d, %d times)   recipe: %s' % (p['id'], a, b, p['v'][0], a, b, rc)
    return '#%d  %d turned %d time%s = %s   (every unit of %d takes %d i-turns)   recipe: %s' % (
        p['id'], a, b, '' if b == 1 else 's', value_text(tuple(p['v'])), a, b, rc)


# ---------------- division: split, regroup and count ----------------

def division_role(m, name, rid, base, count, why):
    if find_role(m, name) is None:
        add_role(m, name, DIV_ROLE_RULE, kind='division', evidence=rid, why=why,
                 recipe=recipe_divide(base, count))


def do_division(m, a, b, manual=False):
    base, count = m['records'][a]['value'], m['records'][b]['value']
    out = zero_gate(m, 'operation', name='regroup', args=(base, count))
    rid = len(m['divisions'])
    rec = {'id': rid, 'l': a, 'r': b, 'recipe': recipe_divide(base, count)}
    if out is None:
        rec.update(status='blocked', reason='division_by_zero', q=None, rem=None, zeros=None, op='regroup')
    else:
        q, rem, zeros = out
        if zeros >= 1:
            division_role(m, 'divide', rid, base, count, 'a 0 was put in to split the units into groups')
        if rem >= 1:
            division_role(m, 'remainder', rid, base, count, 'units were left over after the last full group')
        rec.update(status='done', q=q, rem=rem, zeros=zeros, op='divide' if find_role(m, 'divide') else 'regroup')
    if manual:
        rec['manual'] = True
    zero_gate(m, 'record', record=rec, family='division')
    m['divisions'].append(rec)
    return rec


def division_line(m, d, facing=0):
    a, b = m['records'][d['l']]['value'], m['records'][d['r']]['value']
    if d['status'] == 'blocked':
        return '#%d  %d / %d   blocked: a group of no units can never fill   recipe: %s' % (d['id'], a, b, d['recipe'])
    turned = ' turned %d time%s' % (facing, '' if facing == 1 else 's') if facing else ''
    rc = d['recipe'] if not facing else 'S*%d T*%d R*%d' % (a, facing, b)
    def face(n):                    # n units facing the way the dividend was turned
        return value_text(((1, 0), (0, 1), (-1, 0), (0, -1))[facing % 4] and
                          (n * ((1, 0), (0, 1), (-1, 0), (0, -1))[facing % 4][0],
                           n * ((1, 0), (0, 1), (-1, 0), (0, -1))[facing % 4][1]))
    frac = ' = %s + %s/%d' % (face(d['q']), face(d['rem']), b) if d['rem'] else ''
    return '#%d  %d%s / %d = %s remainder %s%s   units: %s   recipe: %s' % (
        d['id'], a, turned, b, face(d['q']), face(d['rem']), frac, layout_text(d['q'], b, d['rem']), rc)


# ---------------- proofs: hide a number in a true slot filling ----------------

PROOF_WHY = {'proof': 'the number that was hidden was found again',
             'other_answer': 'another x fits the hidden number as well',
             'lost_answer': 'the hidden number did not come back (not reached, or too far away)'}


def proof_parts(m, slot):
    st = slot_state(m, slot['ref'])
    choice = slot_filling(st['symbols'], slot['n'])
    groups, ops = slot_groups(st['symbols'], choice)
    nums, _ = slot_numbers(st['symbols'], choice, slot['limit'])
    return groups, ops, nums


def proof_text(m, slot, g):
    groups, ops, _nums = proof_parts(m, slot)
    out = ''
    for i, gr in enumerate(groups):
        out += 'x' if i == g else gr
        if i < len(ops):
            out += ops[i]
    return '%s = %s' % (out, slot_value_text(slot) if slot['status'] == 'done' else 'blocked')


def recipe_proof(m, slot, g):
    return 'hide %s of [%s]' % ('nothing' if g is None else 'number %d' % g, slot['recipe'])


def proof_candidates(m, orig, n, bound=None, xbound=None):
    top = min(PROOF_BOUND if bound is None else bound, max(XP_BOUND if xbound is None else xbound, abs(orig[0]), abs(orig[1])))
    return [tuple(p['p']) for p in m['planes'][:n] if max(abs(p['p'][0]), abs(p['p'][1])) <= top], top


def proof_search(groups_ops_nums, g, target, cands, binop):
    ops, nums = groups_ops_nums
    xs, over, blocks = [], 0, 0
    for x in cands:
        nn = list(nums)
        nn[g] = x
        res = evaluate_slot(nn, ops, binop)
        if res is None:
            over += 1
        elif isinstance(res, str):
            blocks += 1
        elif res == target:
            xs.append(list(x))
    return xs, over, blocks


def proof_names(rec):
    out = []
    if rec['status'] == 'done':
        out.append('proof' if rec['found_orig'] else 'lost_answer')
        if len([x for x in rec['xs'] if x != rec['orig']]) >= 1:
            out.append('other_answer')
    return out


def do_proof(m, sid, g, manual=False):
    slot = m['slot_log'][sid]
    rid = len(m['proofs'])
    if slot['status'] == 'blocked':
        rec = {'id': rid, 'slot': sid, 'g': None, 'status': 'blocked', 'text': proof_text(m, slot, None),
               'why': slot['why'], 'op': 'prove', 'recipe': recipe_proof(m, slot, None)}
    else:
        groups, ops, nums = proof_parts(m, slot)
        orig = nums[g]
        n, limit = len(m['planes']), len(m['records'])
        cands, top = proof_candidates(m, orig, n)
        target = (slot['value'], slot['im'], slot['den'])
        xs, over, blocks = proof_search((ops, nums), g, target, cands,
                                        lambda op, a, b: zero_gate(m, 'operation', name='slotop', args=(op, a, b, limit)))
        rec = {'id': rid, 'slot': sid, 'g': g, 'status': 'done', 'text': proof_text(m, slot, g), 'orig': list(orig),
               'xs': xs, 'found_orig': list(orig) in xs, 'over': over, 'blocks': blocks, 'tried': len(cands),
               'bound': top, 'n': n, 'limit': limit, 'pb': PROOF_BOUND, 'xb': XP_BOUND, 'op': 'prove', 'recipe': recipe_proof(m, slot, g)}
    if manual:
        rec['manual'] = True
    for name in proof_names(rec):
        if find_role(m, name) is None:
            add_role(m, name, PROOF_RULE, kind='proof', evidence=rid, why=PROOF_WHY[name], recipe=rec['recipe'])
    zero_gate(m, 'record', record=rec, family='proof')
    m['proofs'].append(rec)
    return rec


def run_proofs(m, budget):
    """Walk the true slot fillings in order and hide each of their numbers in turn. A filling that is
    still parked is waited for, never skipped."""
    made = 0
    c = m['proof_cur']
    log = m['slot_log']
    while made < budget and c[0] < len(log) and not STOP['flag']:
        slot = log[c[0]]
        if slot['status'] == 'parked':
            break
        if slot['status'] == 'blocked':
            do_proof(m, c[0], None)
            c[0], c[1] = c[0] + 1, 0
        else:
            ngroups = len(proof_parts(m, slot)[1]) + 1
            do_proof(m, c[0], c[1])
            if c[1] + 1 >= ngroups:
                c[0], c[1] = c[0] + 1, 0
            else:
                c[1] += 1
        made += 1
    return made


def proof_line(m, p):
    if p['status'] == 'blocked':
        return '#%d  %s   (slot filling #%d is blocked, so nothing is hidden)   recipe: %s' % (p['id'], p['text'], p['slot'], p['recipe'])
    got = ', '.join(value_text(tuple(x)) for x in p['xs'][:5]) + (' ...' if len(p['xs']) > 5 else '') if p['xs'] else 'nothing'
    return '#%d  %s   hid %s: found %s%s (tried %d points out to %d)   recipe: %s' % (
        p['id'], p['text'], value_text(tuple(p['orig'])), got,
        '  -> came back' if p['found_orig'] else '  -> did not come back', p['tried'], p['bound'], p['recipe'])


def proof_status(m):
    ps = m['proofs']
    d = [p for p in ps if p['status'] == 'done']
    return '  Proofs: %d (%d came back, %d lost, %d with another answer too, %d blocked) | roles found: %s' % (
        len(ps), sum(1 for p in d if p['found_orig']), sum(1 for p in d if not p['found_orig']),
        sum(1 for p in d if any(x != p['orig'] for x in p['xs'])), sum(1 for p in ps if p['status'] == 'blocked'),
        ', '.join(r['name'] for r in m['roles'] if r.get('kind') == 'proof') or 'none yet')


# ---------------- x on the plane ----------------

PUNKNOWN_WHY = {'undo_zero': 'going backwards lands on Z0 and the answer is Z0 too: zero is named like every other answer',
                'imaginary_answer': 'the x that fits is a pure i number',
                'complex_answer': 'the x that fits has a real part and an i part',
                'every_point': 'every plane point tried fits the blank',
                'undo_turn': 'turning the answer back (going backwards) lands on the same point'}
UNIT_TURNS = ((0, 1), (-1, 0), (0, -1))


def px_candidates(m, a, c, n, bound=None):
    top = min(XP_BOUND if bound is None else bound, max(abs(a[0]), abs(a[1]), abs(c[0]), abs(c[1])) + 2)
    return [tuple(p['p']) for p in m['planes'][:n] if max(abs(p['p'][0]), abs(p['p'][1])) <= top]


def psolve(cands, a, c, ev, back):
    forms = []
    for op, side in UNKNOWN_FORMS:
        xs, over, dz, nonint = [], 0, 0, 0
        for x in cands:
            res = ev(op, a if side == 'R' else x, x if side == 'R' else a)
            if res is None:
                over += 1
            elif res == 'DIV0':
                dz += 1
            elif res == 'NONINT':
                nonint += 1
            elif res == c:
                xs.append(list(x))
        b = back(op, side)
        forms.append({'op': op, 'side': side, 'xs': xs, 'over': over, 'dz': dz, 'nonint': nonint,
                      'back': None if b is None else list(b), 'ok': b is not None and list(b) in xs})
    return forms


def punknown_names(f, a, ncand):
    out = []
    if any(x[0] == 0 and x[1] != 0 for x in f['xs']):
        out.append('imaginary_answer')
    if any(x[0] != 0 and x[1] != 0 for x in f['xs']):
        out.append('complex_answer')
    if f['xs'] and len(f['xs']) == ncand and ncand > 1:
        out.append('every_point')
    if f['ok'] and f['op'] in '*/' and tuple(a) in UNIT_TURNS:
        out.append('undo_zero' if f['back'] == [0, 0] else 'undo_turn')
    return out


def punknown_role_x(name, f):
    if name == 'imaginary_answer':
        return [x for x in f['xs'] if x[0] == 0 and x[1] != 0][0]
    if name == 'complex_answer':
        return [x for x in f['xs'] if x[0] != 0 and x[1] != 0][0]
    if name in ('undo_turn', 'undo_zero'):
        return f['back']
    return f['xs'][0]


def px_point_recipe(m, p):
    if p is None:
        return 'none'
    pid = plane_seen(m).get(tuple(p))
    return value_text(tuple(p)) if pid is None else m['planes'][pid]['recipe']


def recipe_punknown(m, op, side, a, c, x):
    ar, cr, xr = px_point_recipe(m, a), px_point_recipe(m, c), px_point_recipe(m, x)
    left = '(%s) %sX' % (ar, op) if side == 'R' else 'X%s (%s)' % (op, ar)
    return '%s = (%s) : X=(%s)' % (left, cr, xr)


def recipe_punknown_pair(m, l, r):
    return '(%s) ; (%s) ; X' % (m['planes'][l]['recipe'], m['planes'][r]['recipe'])


def do_punknown(m, l, r, manual=False):
    a, c = tuple(m['planes'][l]['p']), tuple(m['planes'][r]['p'])
    n, limit = len(m['planes']), len(m['records'])
    cands = px_candidates(m, a, c, n)
    forms = psolve(cands, a, c,
                   lambda op, A, B: zero_gate(m, 'operation', name='cplx', args=(op, A, B, limit)),
                   lambda op, side: zero_gate(m, 'operation', name='undo2', args=(op, side, a, c)))
    rid = len(m['punknowns'])
    rec = {'id': rid, 'l': l, 'r': r, 'n': n, 'limit': limit, 'tried': len(cands), 'forms': forms,
           'recipe': recipe_punknown_pair(m, l, r), 'op': 'try', 'xp': XP_BOUND}
    if manual:
        rec['manual'] = True
    for fi, f in enumerate(forms):
        for name in punknown_names(f, a, len(cands)):
            if find_role(m, name) is None:
                add_role(m, name, XP_ROLE_RULE, kind='punknown', evidence=rid, form=fi, why=PUNKNOWN_WHY[name],
                         recipe=recipe_punknown(m, f['op'], f['side'], a, c, punknown_role_x(name, f)))
    zero_gate(m, 'record', record=rec, family='punknown')
    m['punknowns'].append(rec)
    return rec


def pform_text(f, a, c, show=5, tried=None, dead=False):
    at = value_text(a)
    at = '(%s)' % at if a[1] != 0 and a[0] != 0 else at
    left = '%s%sx' % (at, f['op']) if f['side'] == 'R' else 'x%s%s' % (f['op'], at)
    xs = f['xs']
    if not xs:
        ans = ('no point among the %d tried fits' % len(tried) if tried is not None else 'no reached point fits') \
            + (' (%d outgrew the counter)' % f['over'] if f['over'] else '')
    else:
        ans = 'x = ' + ', '.join(value_text(tuple(x)) for x in xs[:show]) + (' ... (%d fit)' % len(xs) if len(xs) > show else '')
    off = f['back'] is not None and not f['ok'] and tried is not None and tuple(f['back']) not in tried
    back = '' if f['back'] is None else '   backwards: %s%s' % (
        value_text(tuple(f['back'])), ' (same)' if f['ok'] else ' (DEADLOCK: a blocked move, so the path cannot continue)' if dead
        else ' (not among those tried)' if off else ' (different)')
    return '%s = %s   %s%s' % (left, value_text(c), ans, back)


def punknown_line(m, u, only=None):
    a, c = tuple(m['planes'][u['l']]['p']), tuple(m['planes'][u['r']]['p'])
    lines = ['#%d  plane blank for %s and %s (tried %d of the %d points reached, counter %d)   recipe: %s'
             % (u['id'], value_text(a), value_text(c), u['tried'], u['n'], u['limit'], u['recipe'])]
    for f in u['forms']:
        if only is None or (f['op'], f['side']) == only:
            lines.append('      ' + pform_text(f, a, c, tried=set(px_candidates(m, a, c, u['n'], u.get('xp', XP_BOUND))),
                                        dead=deadlock_hit(m, 'punknown', u, f)))
    return '\n'.join(lines)


def parse_equation(text):
    """i*x=1  or  x+2i=3-i  ->  (op, side, A, C) or None"""
    s = text.replace(' ', '').lower()
    if s.count('=') != 1 or s.count('x') != 1:
        return None
    left, right = s.split('=')
    if 'x' not in left:
        return None
    if left.startswith('x') and len(left) > 2 and left[1] in '+-*/':
        op, side, a = left[1], 'L', left[2:]
    elif left.endswith('x') and len(left) > 2 and left[-2] in '+-*/':
        op, side, a = left[-2], 'R', left[:-2]
    else:
        return None
    A, C = parse_value(a), parse_value(right)
    if A is None or C is None:
        return None
    return op, side, A, C


def lookup_punknown(m, text, force=False):
    eq = parse_equation(text)
    if eq is None:
        return False
    op, side, A, C = eq
    if not force and A[1] == 0 and C[1] == 0 and A[0] >= 0 and C[0] >= 0:
        return False                       # counted numbers only: the counter blank handles it. A negative goes to the plane.
    seen = plane_seen(m)
    print('\nPlane blank in %s:' % text.strip())
    missing = [v for v in (A, C) if v not in seen]
    if missing:
        for v in missing:
            print('  The point %s has not been reached on the plane yet.' % value_text(v))
            want_check(m, ('plane', v[0], v[1]), False)
        return True
    l, r = seen[A], seen[C]
    hits = [u for u in m['punknowns'] if (u['l'], u['r']) == (l, r)]
    print('  Tried by the engine %d time(s)' % len(hits))
    for u in hits[:3]:
        print('  ' + punknown_line(m, u, (op, side)).replace('\n', '\n  '))
    if not hits:
        print('  Not tried yet (pairs go in order). Type: solve %s  to try it now.' % text.strip())
    want_check(m, ('pblank', A[0], A[1], C[0], C[1]), bool(hits))
    return True


def punknown_status(m):
    return '  Plane blanks: %d pairs tried | roles found: %s' % (
        len(m['punknowns']), ', '.join(r['name'] for r in m['roles'] if r.get('kind') == 'punknown') or 'none yet')


# ---------------- WANTED: what was asked for and not found ----------------

WANT_SEEN = {}       # key tuple -> want id. Rebuilt when the sizes disagree.


def want_seen(m):
    if not cache_fresh('want', m['wanted']):
        WANT_SEEN.clear()
        for w in m['wanted']:
            WANT_SEEN[tuple(w['key'])] = w['id']
        cache_stamp('want', m['wanted'])
    return WANT_SEEN


def want_text(key):
    k = key[0]
    if k == 'count':
        return 'counter number %d' % key[1]
    if k == 'path':
        return 'value %s on an S-and-turn path' % value_text((key[1], key[2]))
    if k == 'plane':
        return 'plane point %s' % value_text((key[1], key[2]))
    if k == 'blank':
        return 'blank search for the pair %d and %d' % (key[1], key[2])
    if k == 'slot':
        return 'slot filling that gives %s' % (str(key[1]) if key[2] == 1 else mixed('-' if key[1] < 0 else '', 0, abs(key[1]), key[2]))
    if k == 'cslot':
        return 'slot filling that lands on the point %s' % value_text((key[1], key[2]))
    if k == 'pblank':
        return 'plane blank search for the points %s and %s' % (value_text((key[1], key[2])), value_text((key[3], key[4])))
    if k == 'select':
        return 'negative selector: %s %d' % (key[1], key[2])
    if k == 'pause':
        return 'pair exploration paused until something new arrives (counter at %d)' % key[1]
    if k == 'fracq':
        return 'leftover fraction %s written as typed (%d of %d)' % (mixed('', key[1], key[2], key[3]), key[2], key[3])
    return 'leftover fraction %s' % mixed('', key[1], key[2], key[3])


def recipe_wanted(key):
    return 'W ' + want_text(key)


def want_match(m, key, ptr):
    """Does the record pointed at really answer this want?"""
    k, kind, i = key[0], ptr[0], ptr[1]
    if k == 'select':
        return False                     # a negative selector points at nothing, so nothing can answer it yet
    if k == 'pause':
        return kind == 'record' and pause_sig(m) != list(key[1:])
    try:
        if k == 'count':
            return kind == 'record' and m['records'][i]['value'] == key[1]
        if k == 'path':
            return kind == 'node' and node_value(m['nodes'][i]['c']) == (key[1], key[2])
        if k == 'plane':
            return kind == 'plane' and tuple(m['planes'][i]['p']) == (key[1], key[2])
        if k == 'blank':
            u = m['unknowns'][i]
            return kind == 'blank' and (u['l'], u['r']) == (key[1], key[2])
        if k == 'slot':
            r = m['slot_log'][i]
            return kind == 'slot' and r['status'] == 'done' and (r['value'], r['im'], r['den']) == (key[1], 0, key[2])
        if k == 'fraction':
            return kind == 'fraction' and m['fractions'][i]['key'] == [key[1], key[2], key[3]]
        if k == 'fracq':
            f = m['fractions'][i]
            return kind == 'fraction' and (f['q'], f['r'], f['b']) == (key[1], key[2], key[3])
        if k == 'cslot':
            r = m['slot_log'][i]
            return kind == 'slot' and r['status'] == 'done' and (r['value'], r['im'], r['den']) == (key[1], key[2], 1)
        if k == 'pblank':
            u = m['punknowns'][i]
            return kind == 'pblank' and (tuple(m['planes'][u['l']]['p']), tuple(m['planes'][u['r']]['p'])) == \
                ((key[1], key[2]), (key[3], key[4]))
    except (IndexError, KeyError, TypeError):
        return False
    return False


def want_answer(m, key):
    """What answers this want now, as a pointer, or None."""
    k = key[0]
    if k == 'select':
        return None                      # kept open, for the zero gate to use later
    if k == 'pause':
        return None if pause_sig(m) == list(key[1:]) else ('record', len(m['records']) - 1)
    if k == 'count':
        return ('record', key[1]) if key[1] < len(m['records']) else None
    if k == 'path':
        ids = NODE_INDEX.get((key[1], key[2]))
        return ('node', ids[0]) if ids else None
    if k == 'plane':
        pid = plane_seen(m).get((key[1], key[2]))
        return None if pid is None else ('plane', pid)
    if k == 'blank':
        for u in m['unknowns']:
            if (u['l'], u['r']) == (key[1], key[2]):
                return ('blank', u['id'])
        return None
    if k == 'slot':
        for r in m['slot_log']:
            if r['status'] == 'done' and (r['value'], r['im'], r['den']) == (key[1], 0, key[2]):
                return ('slot', r['id'])
        return None
    if k == 'cslot':
        for r in m['slot_log']:
            if r['status'] == 'done' and (r['value'], r['im'], r['den']) == (key[1], key[2], 1):
                return ('slot', r['id'])
        return None
    if k == 'fracq':
        for f in m['fractions']:
            if (f['q'], f['r'], f['b']) == (key[1], key[2], key[3]):
                return ('fraction', f['id'])
        return None
    if k == 'pblank':
        for u in m['punknowns']:
            if (tuple(m['planes'][u['l']]['p']), tuple(m['planes'][u['r']]['p'])) == ((key[1], key[2]), (key[3], key[4])):
                return ('pblank', u['id'])
        return None
    for f in m['fractions']:
        if f['key'] == [key[1], key[2], key[3]]:
            return ('fraction', f['id'])
    return None


def negative_selector(m, command, n):
    """A negative number points at no record. It is kept in the wanted archive, not shown as the newest record."""
    if n >= 0:
        return False
    print('  %s %d: a negative number does not point at any record. It is kept in the wanted archive.' % (command, n))
    want_check(m, ('select', command, n), False)
    return True


def want_check(m, key, found):
    """Called by every lookup. Empty -> kept in the wanted archive. Found -> says if it was wanted before."""
    seen = want_seen(m)
    if key in seen:
        w = m['wanted'][seen[key]]
        if found and w['status'] == 'found':
            by = w['by']
            print('  Wanted before: asked %d time(s), first answered in run %d by %s #%d.'
                  % (w['asks'], w['found_run'], by[0], by[1]))
            return
        if not found:
            w['asks'] += 1
            zero_gate(m, 'update', record=w)
            print('  Still wanted (#%d): asked %d time(s) now. It stays in the wanted archive.' % (w['id'], w['asks']))
            return
        return
    if found:
        return
    w = {'id': len(m['wanted']), 'key': list(key), 'text': want_text(key), 'status': 'open', 'asks': 1,
         'by': None, 'found_run': None, 'recipe': recipe_wanted(key), 'op': 'want'}
    zero_gate(m, 'record', record=w, family='want')
    m['wanted'].append(w)
    seen[key] = w['id']
    print('  Saved to the wanted archive (#%d: %s). The engine checks it every run.' % (w['id'], w['text']))


def resolve_wanted(m):
    n = 0
    for w in m['wanted']:
        if w['status'] != 'open':
            continue
        ptr = want_answer(m, tuple(w['key']))
        if ptr is not None:
            w['status'], w['by'], w['found_run'] = 'found', list(ptr), m['runs'] + 1
            zero_gate(m, 'update', record=w)
            n += 1
    return n


def wanted_status(m):
    ws = m['wanted']
    return '  Wanted: %d in all | %d still open | %d found since' % (
        len(ws), sum(1 for w in ws if w['status'] == 'open'), sum(1 for w in ws if w['status'] == 'found'))


# ---------------- CORRECTIONS: every caught error is kept ----------------

CORRECTION_WHO = ('Luke', 'tests', 'Dragon Z v15', 'Dragon Z v14.1', 'Dragon Z v19', 'Dragon Z v23.1')
CORRECTIONS_SEED = (
    ('Luke', 'claim', 'E (energy) was put in before the S core was finished', 'v3: built from v1 with E shelved; E waits until S is perfect'),
    ('tests', 'code', 'joined digit strings such as 111101111 made the counter try to reach about 111 million and the phone ran out of memory', 'v5: a number can only be used once the counter has reached it; until then the filling is parked and retried'),
    ('Luke', 'code', 'the multiply role skipped 0 x 2 = 0, throwing away a real path', 'v6.1: zero paths count as multiplication evidence again'),
    ('tests', 'code', 'hand-made multiplication records broke the pair-order replay check', 'v6: manual records are flagged and sit outside the pair order'),
    ('tests', 'code', 'a turned quotient showed 3 where it should have shown -3', 'v9: the quotient and remainder are shown facing the way the dividend was turned'),
    ('Dragon Z v15', 'code', 'undo_turn was first found on the zero case i*x=0, which hid the real turn case', 'v15: undo_turn needs a non-zero answer; v17 added undo_zero so zero is named too'),
    ('tests', 'code', 'a tampered role crashed the replay instead of failing with a clear message', 'v15: a role that points at a record that does not show it fails the replay by name'),
    ('Dragon Z v14.1', 'code', 'the plane picture labels left out the minus signs', 'v14.1: labels show -4 -3 -2 -1 0 1 2 3 4'),
    ('Luke', 'claim', 'it was claimed the engine had found Euclid when the chain of leftovers was a function written for it', 'v18: the engine follows its own division records to find the fewest parts'),
    ('Luke', 'code', 'the T turn cut the turn count down by fours, so five turns matching one turn was the code and not the engine', 'v18: T turns the units one turn at a time'),
    ('Dragon Z v19', 'code', 'joined digit groups were read with Python int() and marks of i were cut down by a remainder of four', 'v19: groups are counted with repeated adds and S steps, and each i mark is one literal turn'),
    ('Luke', 'claim', 'it was claimed that going backwards was found by the engine when the backwards methods were written for it', 'v20: provenance separates the rule, the procedure and what the engine earned'),
    ('Dragon Z v23.1', 'code', 'the engine saved the loaded archive before checking it, so a bad file could be written over the good backup', 'v23.1: the archive is replayed from 0 before any work or save; a failing file is kept under its own name and nothing is written over a good backup'),
    ('Dragon Z v23.1', 'code', 'a main file that was readable but not an archive crashed the loader, and two bad files started a fresh archive', 'v23.1: each file is checked for shape and replay, the backup is tried, and if neither passes the engine stops and changes nothing'),
    ('Dragon Z v23.1', 'code', 'a damaged reference crashed the replay, and a path node that was its own parent made it never finish', 'v23.1: references are checked before they are followed, a parent must be an earlier node, and any crash becomes a reported problem'),
    ('Dragon Z v23.1', 'code', 'a typed fraction with a huge numerator ran a loop with no limit and skipped the zero gate', 'v23.1: both numbers must already be counted; otherwise the want is kept in the wanted archive'),
    ('Dragon Z v23.1', 'code', 'show -1, slot -1 and node -1 displayed the newest record', 'v23.1: a negative selector shows nothing and is kept in the wanted archive for later use by the zero gate'),
)


def correction_recipe(what):
    return 'C ' + what[:60]


def add_correction(m, who, kind, what, fix, seeded=False):
    rec = {'id': len(m['corrections']), 'who': who, 'kind': kind, 'what': what, 'fix': fix,
           'seeded': seeded, 'op': 'correction', 'recipe': correction_recipe(what)}
    zero_gate(m, 'record', record=rec, family='correction')
    m['corrections'].append(rec)
    return rec


def seed_corrections(m):
    if m['corrections']:
        return
    for who, kind, what, fix in CORRECTIONS_SEED:
        add_correction(m, who, kind, what, fix, seeded=True)


def upgrade_credits(m):
    """An archive from before v23.13 holds seeded corrections labelled with another name. Each is relabelled with the Dragon Z version it was fixed in,
    and each change is a Z0 stamp, so nothing is changed without a record of it."""
    n = 0
    for k, c in enumerate(m.get('corrections', [])):
        if isinstance(c, dict) and c.get('seeded') is True and k < len(CORRECTIONS_SEED)                 and CORRECTIONS_SEED[k][0].startswith('Dragon Z v') and c.get('who') != CORRECTIONS_SEED[k][0]:
            old = len(c.get('z0u', []))
            c['who'] = CORRECTIONS_SEED[k][0]
            note_change(m, c, old, {'who': c['who']})
            n += 1
    return n


def correction_line(c):
    return '#%d  caught by %s (%s): %s\n      fixed: %s' % (c['id'], c['who'], c['kind'], c['what'], c['fix'])


def correction_status(m):
    cs = m['corrections']
    return '  Corrections: %d kept (caught by Luke %d, tests %d, a Dragon Z version %d)' % (
        len(cs), sum(1 for c in cs if c['who'] == 'Luke'), sum(1 for c in cs if c['who'] == 'tests'),
        sum(1 for c in cs if c['who'] not in ('Luke', 'tests')))


def replay_corrections(m):
    problems = []
    cs = m['corrections']
    z = zero_state(m)
    if len(cs) < len(CORRECTIONS_SEED):
        problems.append('caught errors were removed: %d kept but %d were written in' % (len(cs), len(CORRECTIONS_SEED)))
    for k, c in enumerate(cs):
        if c.get('id') != k or c['who'] not in CORRECTION_WHO or c['kind'] not in ('claim', 'code'):
            problems.append('correction %d is out of order or has an unknown source' % k)
        if k < len(CORRECTIONS_SEED):
            who, kind, what, fix = CORRECTIONS_SEED[k]
            if (c['who'], c['kind'], c['what'], c['fix'], c.get('seeded')) != (who, kind, what, fix, True):
                problems.append('correction %d was edited' % k)
        elif c.get('seeded'):
            problems.append('correction %d claims to be written in but is not' % k)
        if 'z0' not in c:
            problems.append('correction %d never passed through Z0' % k)
        if len(problems) >= 20:
            problems.append('... more problems not listed')
            return problems
    st_ = [c['z0'] for c in cs if 'z0' in c]
    if len(set(st_)) != len(st_) or z['correction_passages'] != len(cs):
        problems.append('Z0 passage numbers for corrections do not match')
    return problems


# ---------------- PROVENANCE: whose is what ----------------

PROVENANCE = (
    ('the counter', "S counts up from Z0; everything passes back through Z0 (Luke)",
     'S(n) = n + 1 is given; zero_gate is the coded form of the rule', [], 'records'),
    ('the i turn', 'i is a turn action: +1 -> +i -> -1 -> -i (Luke)',
     'turn(d), unit_step', ['half_turn', 'right_turn', 'full_turn'], 'nodes'),
    ('addition', 'addition must emerge from S walks (Luke)', 'walk / repeat_S', ['add'], 'expressions'),
    ('subtraction and negatives', 'a unit meeting its opposite cancels back to Z0 (Luke)', 'unit_step, signed_walk',
     ['subtract', 'negative', 'minus_i', 'imaginary'], 'nodes'),
    ('multiplication', 'repeat the action; zero paths are kept, 0 x 2 = 0 (Luke)', 'repeat_add', ['multiply'], 'products'),
    ('rotation', 'turn every unit b times; four turns cancel (Luke)', 'repeat_turn, turn_units', ['rotate'], 'products'),
    ('division', '00404: split into 1s with 0s between and count the splits (Luke)', 'regroup',
     ['divide', 'remainder'], 'divisions'),
    ('fractions', 'the leftover is a part of a group', 'fraction_chain follows the divisions archive',
     ['fraction', 'reduce'], 'fractions'),
    ('the 00404 slots', '00404 breaks into units and zeros with a slot between each (Luke)',
     'slot_filling, slotop, group_point (counted), run_slots', [], 'slot_log'),
    ('x as the unknown', 'x is a blank that is tried; a proof where the expression is related, a new equation only when written (Luke)',
     'solve_pair, psolve, undo / undo2 (the backwards steps), cplx',
     ['unknown', 'negative_answer', 'any_answer', 'no_answer', 'undo_add', 'undo_subtract', 'undo_multiply',
      'undo_divide'], 'unknowns'),
    ('x on the plane (i turns)', 'x reaches the i turns and the plane (Luke)', 'psolve, cplx, undo2',
     ['imaginary_answer', 'complex_answer', 'every_point', 'undo_turn', 'undo_zero'], 'punknowns'),
    ('proofs in the slots', 'hide a number in a true filling and find it again', 'proof_search',
     ['proof', 'other_answer', 'lost_answer'], 'proofs'),
    ('the plane', 'the plane and its dimensions must be seen by the engine through Z0 (Luke)', 'scan_plane, look',
     ['plane', 'quadrant_1', 'quadrant_2', 'quadrant_3', 'quadrant_4'], 'planes'),
    ('caught errors are an archive', 'every error is kept, with who caught it (Luke)', 'add_correction, replay_corrections', [], 'corrections'),
    ('not found is an archive', 'nothing is lost, a miss is kept and used again (Luke)', 'want_check, resolve_wanted', [], 'wanted'),
    ('deadlocks are an archive', 'a way back that hits a blocked move is kept, not hidden or turned into nothing (Luke)',
     'do_deadlocks, deadlock_hit, replay_deadlocks', [], 'deadlocks'),
    ('tangents are an archive', 'every branch off a main path is kept once, wherever it ends (Luke)',
     'do_tangents, branch_step, replay_tangents', [], 'tangents'),
    ('approaches are an archive', 'a path that closes in on a value without arriving is kept apart from the stuck ones (Luke)',
     'do_approaches, approach_test, replay_approaches', [], 'approaches'),
    ('differences are an archive', 'the change between neighbours is found by climbing, and kept, even when it is nothing (Luke)',
     'do_differences, climb, replay_differences', [], 'differences'),
    ('totals are an archive', 'smaller parts are stacked onto a bigger whole, each stack built on the one before it (Luke)',
     'do_totals, stack_up, replay_totals', [], 'totals'),
)
PYTHON_STILL = (
    'whether a number is below zero or equal to zero (sign and size checks)',
    'how far the blank and the proofs try (phone-safety limits such as a+c+2)',
    'the order the cursors walk the pairs',
    'the method of each backwards step (undo, undo2)',
    'the helper that keeps slot fractions small (reduce_part)',
    'reading digits of what you type, and printing',
    'the digits of a slot template: Python str() and int() turn numbers into text and back (breakdown)',
    'the minus sign inside rational (Python negation); cplx uses the engine\'s own away()',
    'undo2 uses 10**9 as "no limit" for its backwards steps',
    'signed_walk reads each result with Python subtraction (c[0] - c[2])',
)


def show_provenance(m):
    print('\nPROVENANCE - whose is what. EARNED is read from the live archives.')
    for name, rule, proc, roles, arch in PROVENANCE:
        print('\n%s' % name.upper())
        print('  RULE      %s' % rule)
        print('  PROCEDURE %s' % proc)
        n = len(m[arch])
        found = [find_role(m, r) for r in roles]
        got = [r for r in found if r is not None]
        line = '%d records in %s' % (n, arch)
        if roles:
            line += ' | roles earned %d of %d' % (len(got), len(roles))
        print('  EARNED    %s' % line)
        for r in got:
            print('            %s - run %s, recipe: %s' % (r['name'], r.get('run', '?'), r.get('recipe', '')))
        missing = [r for r, f in zip(roles, found) if f is None]
        if missing:
            print('            not earned yet: %s' % ', '.join(missing))
    print('\nSTILL PYTHON, NOT THE ENGINE:')
    for p in PYTHON_STILL:
        print('  - ' + p)


# ---------------- the plane: every point reached ----------------

PLANE_SEEN = {}      # (real, imaginary) -> plane id. Rebuilt when the sizes disagree.
QUADRANT = {(1, 1): 'quadrant_1', (-1, 1): 'quadrant_2', (-1, -1): 'quadrant_3', (1, -1): 'quadrant_4'}
PLANE_WHY = {'plane': 'a point with a real part AND an i part: two directions at once',
             'quadrant_1': 'first point in the quarter with real + and i +',
             'quadrant_2': 'first point in the quarter with real - and i +',
             'quadrant_3': 'first point in the quarter with real - and i -',
             'quadrant_4': 'first point in the quarter with real + and i -'}


def plane_seen(m):
    if not cache_fresh('plane', m['planes']):
        PLANE_SEEN.clear()
        for p in m['planes']:
            PLANE_SEEN[tuple(p['p'])] = p['id']
        cache_stamp('plane', m['planes'])
    return PLANE_SEEN


def plane_place(v):
    re_, im = v
    if v == (0, 0):
        return 'Z0'
    if im == 0:
        return '+1 axis' if re_ > 0 else '-1 axis'
    if re_ == 0:
        return '+i axis' if im > 0 else '-i axis'
    return QUADRANT[(1 if re_ > 0 else -1, 1 if im > 0 else -1)].replace('_', ' ')


def plane_role_names(v):
    if v[0] != 0 and v[1] != 0:
        return ['plane', QUADRANT[(1 if v[0] > 0 else -1, 1 if v[1] > 0 else -1)]]
    return []


def scan_plane(m, budget):
    """Look at the path nodes in order. A point never reached before becomes a plane record."""
    seen = plane_seen(m)
    nodes, made = m['nodes'], 0
    steps = 0
    while m['plane_cur'] < len(nodes) and steps < budget:
        node = nodes[m['plane_cur']]
        m['plane_cur'] += 1
        steps += 1
        v = node_value(node['c'])
        if v in seen:
            continue
        rec = {'id': len(m['planes']), 'p': [v[0], v[1]], 'node': node['id'], 'place': plane_place(v),
               'op': 'point', 'recipe': recipe_node(m, node['id'])}
        zero_gate(m, 'record', record=rec, family='plane')
        m['planes'].append(rec)
        seen[v] = rec['id']
        for name in plane_role_names(v):
            if find_role(m, name) is None:
                add_role(m, name, PLANE_RULE, kind='plane', evidence=rec['id'], why=PLANE_WHY[name],
                         recipe=rec['recipe'])
        made += 1
    return made


def do_look(m, r):
    n = len(m['planes'])
    rows = zero_gate(m, 'operation', name='look', args=(r, tuple(tuple(p['p']) for p in m['planes']), 2))
    rec = {'id': len(m['views']), 'r': r, 'n': n, 'rows': rows, 'op': 'look', 'fmt': 2,
           'recipe': 'S*%d I*2 S*%d' % (r, r)}
    zero_gate(m, 'record', record=rec, family='view')
    m['views'].append(rec)
    return rec


def plane_status(m):
    pl = m['planes']
    places = {}
    for p in pl:
        places[p['place']] = places.get(p['place'], 0) + 1
    far = max([max(abs(p['p'][0]), abs(p['p'][1])) for p in pl] or [0])
    return '  Plane: %d points reached (out to %d from Z0) | %d looks | %s | roles found: %s' % (
        len(pl), far, len(m['views']),
        ', '.join('%s %d' % (k, v) for k, v in sorted(places.items())) or 'none yet',
        ', '.join(r['name'] for r in m['roles'] if r.get('kind') == 'plane') or 'none yet')


def plane_point_info(m, v):
    pid = plane_seen(m).get(v)
    if pid is None:
        print('  On the plane: not reached yet.')
        return
    p = m['planes'][pid]
    print('  On the plane: point #%d, %s, first reached at path node #%d   recipe: %s' % (
        pid, p['place'], p['node'], p['recipe']))


# ---------------- x: a blank that is tried, never solved ----------------

def x_candidates(a, c, limit, make_negative):
    top = min(limit - 1, a + c + 2)
    out = [0]
    for k in range(1, top + 1):
        out.append(k)
        out.append(make_negative(k))
    return out


def solve_pair(a, c, limit, ev, make_negative, back):
    """Try every candidate in every shape. ev(op, A, B) works a sum out, back(op, side) goes backwards."""
    cands = x_candidates(a, c, limit, make_negative)
    forms = []
    for op, side in UNKNOWN_FORMS:
        xs, over, dz = [], 0, 0
        for x in cands:
            res = ev(op, (a, 1) if side == 'R' else (x, 1), (x, 1) if side == 'R' else (a, 1))
            if res is None:
                over += 1
            elif res == 'DIV0':
                dz += 1
            elif res == (c, 1):
                xs.append(x)
        b = back(op, side)
        forms.append({'op': op, 'side': side, 'xs': xs, 'over': over, 'dz': dz, 'back': b,
                      'ok': b is not None and b in xs})
    return len(cands), forms


def xtext(x):
    return 'I*2 S*%d I*2' % -x if x < 0 else recipe_counter(x)


def recipe_unknown(op, side, a, c, x):
    left = 'S*%d %sX' % (a, op) if side == 'R' else 'X%s S*%d' % (op, a)
    return '%s = S*%d : X=%s' % (left, c, 'none' if x is None else xtext(x))


def recipe_unknown_pair(a, c):
    return 'S*%d S*%d X' % (a, c)


def unknown_role_x(name, f):
    if name == 'no_answer':
        return None
    if name.startswith('undo_'):
        return f['back']
    if name == 'negative_answer':
        return [x for x in f['xs'] if x < 0][0]
    return f['xs'][0]


def unknown_role_names(f):
    out = []
    if f['xs']:
        out.append('unknown')
        if any(x < 0 for x in f['xs']):
            out.append('negative_answer')
    return out


def unknown_all_names(f, n_cands):
    out = unknown_role_names(f)
    if f['xs'] and len(f['xs']) == n_cands:
        out.append('any_answer')
    if not f['xs'] and f['over'] == 0 and f['dz'] == 0:
        out.append('no_answer')
    if f['ok']:
        out.append(UNDO_ROLE[f['op']])
    return out


def do_unknown(m, a, b, manual=False):
    av, cv = m['records'][a]['value'], m['records'][b]['value']
    limit = len(m['records'])
    ncand, forms = solve_pair(
        av, cv, limit,
        lambda op, A, B: zero_gate(m, 'operation', name='rational', args=(op, A, B, limit)),
        lambda k: zero_gate(m, 'operation', name='signed_walk', args=(0, k, 2)),
        lambda op, side: zero_gate(m, 'operation', name='undo', args=(op, side, av, cv)))
    rid = len(m['unknowns'])
    rec = {'id': rid, 'l': a, 'r': b, 'limit': limit, 'tried': ncand, 'forms': forms,
           'recipe': recipe_unknown_pair(av, cv), 'op': 'try'}
    if manual:
        rec['manual'] = True
    for fi, f in enumerate(forms):
        for name in unknown_all_names(f, ncand):
            if find_role(m, name) is None:
                add_role(m, name, X_ROLE_RULE, kind='unknown', evidence=rid, form=fi,
                         why=UNKNOWN_WHY[name],
                         recipe=recipe_unknown(f['op'], f['side'], av, cv, unknown_role_x(name, f)))
    zero_gate(m, 'record', record=rec, family='unknown')
    m['unknowns'].append(rec)
    return rec


UNKNOWN_WHY = {'unknown': 'a number put in the blank made the sum true',
               'negative_answer': 'the number that fits is a negative',
               'any_answer': 'every number tried fits the blank',
               'no_answer': 'no number tried fits the blank',
               'undo_add': 'going backwards (taking away) lands on the same number',
               'undo_subtract': 'going backwards (putting back or taking away) lands on the same number',
               'undo_multiply': 'going backwards (regrouping) lands on the same number',
               'undo_divide': 'going backwards (regrouping or repeating) lands on the same number'}


def form_text(f, a, c, show=6, tried=None, dead=False):
    left = '%d%sx' % (a, f['op']) if f['side'] == 'R' else 'x%s%d' % (f['op'], a)
    xs = f['xs']
    if not xs:
        ans = ('no x among the %d tried' % tried if tried else 'no x among those tried') \
            + (' (%d outgrew the counter)' % f['over'] if f['over'] else '')
    elif len(xs) == 1:
        ans = 'x = %d' % xs[0]
    else:
        ans = 'x = ' + ', '.join(str(x) for x in xs[:show]) + (' ... (%d fit)' % len(xs) if len(xs) > show else '')
    top = None if not tried else (tried - 1) // 2
    off = f['back'] is not None and not f['ok'] and top is not None and abs(f['back']) > top
    back = '' if f['back'] is None else '   backwards: %d%s' % (
        f['back'], ' (same)' if f['ok'] else ' (DEADLOCK: a blocked move, so the path cannot continue)' if dead
        else ' (not among those tried)' if off else ' (different)')
    return '%s = %d   %s%s' % (left, c, ans, back)


def unknown_line(m, u, only=None):
    a, c = m['records'][u['l']]['value'], m['records'][u['r']]['value']
    lines = ['#%d  blank for %d and %d (tried %d numbers each shape, counter %d)   recipe: %s'
             % (u['id'], a, c, u['tried'], u['limit'], u['recipe'])]
    for f in u['forms']:
        if only is None or (f['op'], f['side']) == only:
            lines.append('      ' + form_text(f, a, c, tried=u['tried'], dead=deadlock_hit(m, 'unknown', u, f)))
    return '\n'.join(lines)


def lookup_unknown(m, text):
    s = text.replace(' ', '').lower()
    g = re.fullmatch(r'(\d+)([+\-*/])x=(\d+)', s)
    side = 'R'
    if not g:
        g = re.fullmatch(r'x([+\-*/])(\d+)=(\d+)', s)
        if not g:
            return False
        side, op, a, c = 'L', g.group(1), int(g.group(2)), int(g.group(3))
    else:
        a, op, c = int(g.group(1)), g.group(2), int(g.group(3))
    vals = [r['value'] for r in m['records']]
    if a >= len(vals) or c >= len(vals):
        print('\nBoth numbers must already be counted (0 to %d).' % (len(vals) - 1))
        want_check(m, ('count', max(a, c)), False)
        return True
    hits = [u for u in m['unknowns'] if (u['l'], u['r']) == (a, c)]
    print('\nBlank in %s: tried by the engine %d time(s)' % (text.strip(), len(hits)))
    for u in hits[:3]:
        print('  ' + unknown_line(m, u, (op, side)).replace('\n', '\n  '))
    if not hits:
        print('  Not tried yet (pairs go in order). Type: unk %d %d  to try it now.' % (a, c))
    want_check(m, ('blank', a, c), bool(hits))
    return True


def unknown_status(m):
    us = m['unknowns']
    return '  Blanks: %d pairs tried | roles found: %s' % (
        len(us), ', '.join(r['name'] for r in m['roles'] if r.get('kind') == 'unknown') or 'none yet')


# ---------------- fractions: the leftovers of splitting ----------------

def fraction_role(m, name, rid, a, b, g, why):
    if find_role(m, name) is None:
        add_role(m, name, FRAC_ROLE_RULE, kind='fraction', evidence=rid, why=why,
                 recipe=recipe_fraction(a, b, g))


DIV_SEEN = {}        # (group, leftover) values -> division id. Rebuilt when the sizes disagree.


def div_lookup(m, x, y):
    """Find the division of x into groups of y in the engine's own archive."""
    if not cache_fresh('div', m['divisions']):
        DIV_SEEN.clear()
        for d in m['divisions']:
            DIV_SEEN.setdefault((d['l'], d['r']), d['id'])
        cache_stamp('div', m['divisions'])
    did = DIV_SEEN.get((x, y))
    return None if did is None else m['divisions'][did]


def fraction_chain(m, rem, b):
    """Follow the engine's own division records: b by the leftover, that by its leftover, until nothing
    is left. Returns (g, rem over g, b over g, chain of division ids) or None if a record is not made yet."""
    x, y, chain = b, rem, []
    while y:
        d = div_lookup(m, x, y)
        if d is None or d['status'] != 'done':
            return None
        chain.append(d['id'])
        x, y = y, d['rem']
    dr, db = div_lookup(m, rem, x), div_lookup(m, b, x)
    if dr is None or db is None or dr['status'] != 'done' or db['status'] != 'done':
        return None
    return x, dr['q'], db['q'], chain + [dr['id'], db['id']]


def do_fractions(m, budget):
    """Look at each division in order. Where units were left over, that leftover is a
    part of a group: keep it, and follow the engine's own records to the fewest parts it can be written in."""
    made = 0
    divs = m['divisions']
    while m['fcursor'] < len(divs) and made < budget:
        did = m['fcursor']
        d = divs[did]
        if d['status'] != 'done' or d['rem'] < 1:
            m['fcursor'] = did + 1
            continue
        a, b = m['records'][d['l']]['value'], m['records'][d['r']]['value']
        got = fraction_chain(m, d['rem'], b)
        if got is None:
            break                                   # the splits it needs are not made yet: wait, never skip
        m['fcursor'] = did + 1
        g, rr, bb, chain = got
        rid = len(m['fractions'])
        fraction_role(m, 'fraction', rid, a, b, g, 'units left over after the last full group are a part of a group')
        if g >= 2:
            fraction_role(m, 'reduce', rid, a, b, g,
                          'the leftover and the group can be split by the same g, and the part stays the same')
        rec = {'id': rid, 'div': did, 'q': d['q'], 'r': d['rem'], 'b': b, 'g': g, 'rr': rr, 'bb': bb,
               'steps': len(chain) - 2, 'chain': chain, 'key': [d['q'], rr, bb], 'op': 'fraction',
               'recipe': recipe_fraction(a, b, g)}
        zero_gate(m, 'record', record=rec, family='fraction')
        m['fractions'].append(rec)
        made += 1
    return made


def mixed(sign, whole, p, q):
    if whole == 0:
        return '%s%d/%d' % (sign, p, q)
    if sign:
        return '%s(%d + %d/%d)' % (sign, whole, p, q)       # the sign belongs to the whole number
    return '%d + %d/%d' % (whole, p, q)


def fraction_line(m, f, facing=0):
    d = m['divisions'][f['div']]
    a = m['records'][d['l']]['value']
    sign = {0: '', 2: '-'}.get(facing, '')
    same = '' if f['g'] == 1 else '  = %s in fewest parts (split by %d)' % (mixed(sign, f['q'], f['rr'], f['bb']), f['g'])
    return '#%d  %s%d / %d = %s%s   (from division #%d)   recipe: %s' % (
        f['id'], sign, a, f['b'], mixed(sign, f['q'], f['r'], f['b']), same, f['div'], f['recipe'])


def fraction_ways(m, q, rr, bb, facing=0, limit=8):
    hits = [f for f in m['fractions'] if f['key'] == [q, rr, bb]]
    print('  Written as leftovers of splitting: %d way(s)' % len(hits))
    for f in hits[:limit]:
        print('    ' + fraction_line(m, f, facing))
    if len(hits) > limit:
        print('    ... and %d more' % (len(hits) - limit))


def walk_pair(m, a, b):
    """Walk S forward b times from a. Everything goes through Z0."""
    count = m['records'][b]['value']        # b is the count of S steps from 0
    landed = zero_gate(m, 'operation', name='repeat_S', args=(a, count))
    idx = len(m['expressions'])
    role = find_role(m, 'add')
    if role is None and count >= 1:
        # First walk of one or more S steps: addition has been found.
        role = {'id': len(m['roles']), 'name': 'add', 'rule': ADD_ROLE_RULE,
                'built_from': 'S', 'evidence': idx,
                'recipe': recipe_add(m['records'][a]['value'], count)}
        zero_gate(m, 'record', record=role, family='role')
        m['roles'].append(role)
    expr = {'id': idx, 'op': 'add' if role else 'walk', 'l': a, 'r': b,
            'to': landed, 'value': m['records'][landed]['value'],
            'recipe': recipe_add(m['records'][a]['value'], count)}
    zero_gate(m, 'record', record=expr, family='expression')
    m['expressions'].append(expr)
    return expr


def explore(m):
    made = 0
    walked = 0
    turned = 0
    slotted = 0
    freed = 0
    multiplied = 0
    divided = 0
    blanks = 0
    proved = 0
    pblanks = 0
    answered = 0
    tangled = 0
    deadlocked = 0
    approached = 0
    differed = 0
    stacked = 0
    pointed = 0
    fracs = 0
    div_before = len(m['divisions'])
    pfreed = 0
    prod_before = len(m['products'])
    waiting = []
    before = len(m['records'])
    nodes_before = len(m['nodes'])
    GATE['m'] = m
    begin_interrupt()
    try:
        for _ in units(WORK_PER_RUN):
            step(m)
            made += 1
        for _ in units(0 if pair_paused(m) else PAIR_WORK_PER_RUN):
            pair = next_pair(m)
            if pair is None:
                break
            walk_pair(m, *pair)
            walked += 1
        tangled = do_tangents(m, TANGENT_WORK_PER_RUN)
        for _ in units(MUL_WORK_PER_RUN):
            pair = next_pair(m, 'mpairs')
            if pair is None:
                break
            do_product(m, *pair)
            multiplied += 1
        for _ in units(DIV_WORK_PER_RUN):
            pair = next_pair(m, 'dpairs')
            if pair is None:
                break
            do_division(m, *pair)
            divided += 1
        fracs = do_fractions(m, FRAC_WORK_PER_RUN)
        if not slots_waiting(m):
            for _ in units(X_WORK_PER_RUN):
                pair = next_pair(m, 'xpairs')
                if pair is None:
                    break
                do_unknown(m, *pair)
                blanks += 1
        for _ in units(TURN_WORK_PER_RUN):
            expand(m)
            turned += 1
        pointed = scan_plane(m, PLANE_WORK_PER_RUN)
        if not slots_waiting(m):
            for _ in units(XP_WORK_PER_RUN):
                pair = next_pair(m, 'ppairs', len(m['planes']))
                if pair is None:
                    break
                do_punknown(m, *pair)
                pblanks += 1
        deadlocked = do_deadlocks(m, DEADLOCK_WORK_PER_RUN)
        approached = do_approaches(m, APPROACH_WORK_PER_RUN)
        differed = do_differences(m, DIFFERENCE_WORK_PER_RUN)
        stacked = do_totals(m, TOTAL_WORK_PER_RUN)
        slotted, waiting = run_slots(m, SLOT_WORK_PER_RUN)
        pfreed = retry_products(m)
        freed = retry_slots(m)
        proved = run_proofs(m, PROOF_WORK_PER_RUN) if not slots_waiting(m) else 0
        answered = resolve_wanted(m)
        settle_pair_pause(m, walked, tangled)
    except KeyboardInterrupt:
        print('\nStopped hard in the middle of a step. The state is checked before anything is saved.')
    finally:
        end_interrupt()
    if STOP['flag']:
        print('\nStopped at a clean boundary: every step that was started is finished.')
    m['runs'] += 1
    zero_repair(m)
    problems = replay_light(m)
    if problems:
        print('\nRun', m['runs'], 'done but NOT saved: the archive fails its own replay, so the files on disk are untouched.')
    else:
        verified(m)
        save_memory(m)
        print('\nRun', m['runs'], 'done and saved.')
    print('  New counter records this run:', len(m['records']) - before,
          '| pairs walked:', walked)
    print('  Products: %d pairs repeated and turned (%d records) | %d parked ones freed | %d still parked'
          % (multiplied, len(m['products']) - prod_before, pfreed, len(m['mul_parked'])))
    print('  Divisions: %d pairs split and regrouped | %d leftover parts found as fractions' % (divided, fracs))
    print('  Blanks: %d pairs tried for x%s' % (blanks, '' if not slots_waiting(m) else ' (waiting for every operation and fractions to be found first)'))
    print('  Plane blanks: %d pairs of points tried for x | proofs: %d slot numbers hidden and found' % (pblanks, proved))
    print('  Plane: %d new points reached | wanted: %d answered this run' % (pointed, answered))
    print('  Deadlocks: %d new ones kept this run (%d in all)' % (deadlocked, len(m['deadlocks'])))
    print('  Approaches: %d new ones kept this run (%d in all)' % (approached, len(m['approaches'])))
    print('  Differences: %d new changes between neighbouring products kept this run (%d in all)' % (differed, len(m['differences'])))
    print('  Totals: %d new parts stacked onto the whole this run (%d in all)' % (stacked, len(m['totals'])))
    print('  Tangents: %d new branches kept this run (%d in all)%s' % (tangled, len(m['tangents']), ' | pair exploration is PAUSED, waiting for something new' if pair_paused(m) else ''))
    print('  Paths: %d expanded, %d new path nodes' % (turned, len(m['nodes']) - nodes_before))
    if waiting:
        print('  00404 slots are waiting for these to be found first:', ' '.join(waiting))
    else:
        print('  00404 slots: %d fillings tried this run (%d in all) | %d parked ones freed | %d still parked'
              % (slotted, len(m['slot_log']), freed, len(m['slot_parked'])))
    print_stats(m)
    replay_report(m, problems)


# ---------------- REPLAY: the engine checks its own archive ----------------
# An independent check that does not trust the stored numbers. It rebuilds
# the whole count from 0 using only S and compares with what is saved.

ROLE_ARCHIVE = {'unknown': 'unknowns', 'node': 'nodes', 'plane': 'planes', 'punknown': 'punknowns',
                'product': 'products', 'division': 'divisions', 'fraction': 'fractions', 'proof': 'proofs',
                'approach': 'approaches', 'difference': 'differences', 'total': 'totals'}


def ref_ok(v, size):
    return isinstance(v, int) and not isinstance(v, bool) and 0 <= v < size


def replay_structure(m):
    """Before anything is rebuilt: every reference must point at something that exists, and every
    path node must come from an EARLIER node (so no path can loop back on itself)."""
    problems = []
    for fam, key in FAMILIES:
        for k, r in enumerate(m[key]):
            if not isinstance(r, dict):
                problems.append('%s %d is not a record' % (fam, k))
    if problems:
        return problems[:20]
    n = len(m['records'])
    checks = (('expressions', 'expression', (('l', n), ('r', n), ('to', n))),
              ('products', 'product', (('l', n), ('r', n))),
              ('divisions', 'division', (('l', n), ('r', n))),
              ('unknowns', 'blank search', (('l', n), ('r', n))),
              ('punknowns', 'plane blank search', (('l', len(m['planes'])), ('r', len(m['planes'])))),
              ('fractions', 'fraction', (('div', len(m['divisions'])),)),
              ('planes', 'plane point', (('node', len(m['nodes'])),)),
              ('proofs', 'proof', (('slot', len(m['slot_log'])),)))
    for key, name, fields in checks:
        for k, r in enumerate(m[key]):
            for field, size in fields:
                if not ref_ok(r.get(field), size):
                    problems.append('%s %d: %s points at something that does not exist' % (name, k, field))
        if len(problems) >= 20:
            return problems[:20] + ['... more problems not listed']
    for k, nd in enumerate(m['nodes']):
        if nd.get('a') != 'root' and not ref_ok(nd.get('p'), k):
            problems.append('node %d: its parent must be an earlier node' % k)
    for k, r in enumerate(m['roles']):
        ev = r.get('evidence')
        if r.get('given') or ev is None:
            continue
        arch = ROLE_ARCHIVE.get(r.get('kind'), 'expressions' if r.get('name') == 'add' else None)
        if arch is not None and not ref_ok(ev, len(m[arch])):
            problems.append('role %s: its evidence points at a record that does not exist' % r.get('name'))
    for rid in m['slot_parked']:
        if not ref_ok(rid, len(m['slot_log'])):
            problems.append('the parked slot list points at a filling that does not exist')
            break
    for rid in m['mul_parked']:
        if not ref_ok(rid, len(m['products'])):
            problems.append('the parked product list points at a product that does not exist')
            break
    return problems[:20]


# ---------------- a clean stop (Ctrl-C) ----------------
# The first press only raises a flag. Every loop in a run looks at the flag BETWEEN units of work, so a unit
# that was started is always finished and the saved state is whole. A second press stops at once; the
# half-finished state then has to pass the replay before anything is saved.

STOP = {'flag': False, 'old': None}


def _on_interrupt(signum, frame):
    if STOP['flag']:
        signal.signal(signal.SIGINT, signal.default_int_handler)
        raise KeyboardInterrupt
    STOP['flag'] = True
    print('\n  Stop asked for: finishing the step in hand, then saving. Press again to stop at once.')


def begin_interrupt():
    STOP['flag'] = False
    try:
        STOP['old'] = signal.signal(signal.SIGINT, _on_interrupt)
    except (ValueError, OSError):            # not the main thread: the plain behaviour stays
        STOP['old'] = None


def end_interrupt():
    if STOP['old'] is not None:
        try:
            signal.signal(signal.SIGINT, STOP['old'])
        except (ValueError, OSError):
            pass
        STOP['old'] = None


def units(n):
    """range(n) that stops handing out work once a stop has been asked for."""
    for k in range(n):
        if STOP['flag']:
            return
        yield k


# ---------------- replay: the parts of the file that are not records ----------------

def whole_number(x):
    return isinstance(x, int) and not isinstance(x, bool)


def allowed_role_names():
    names = {'add', 'i', SLOT_TEMPLATE, 'multiply', 'rotate', 'divide', 'remainder', 'fraction', 'reduce', 'limit', 'difference', 'group'}
    names |= {n for n, _t, _w in TURN_ROLES}
    for table in (UNKNOWN_WHY, PLANE_WHY, PUNKNOWN_WHY, PROOF_WHY):
        names |= set(table)
    return names


def cursor_problems(c, name, size):
    """One pair cursor {n, i, step}: its shape, and how many steps it says were taken."""
    if not isinstance(c, dict) or set(c) != {'n', 'i', 'step'} or not all(whole_number(v) for v in c.values()):
        return ['the %s cursor is damaged' % name], None
    n, i, s = c['n'], c['i'], c['step']
    if n < 0 or not 0 <= i <= n or not 0 <= s <= (1 if i == n else 2) or n > size:
        return ['the %s cursor holds a position that cannot exist (%r)' % (name, c)], None
    return [], n * n + 2 * i + s


def replay_meta(m):
    """Rule text, counters, clock stamps, run numbers, cursors: everything that is not a record itself."""
    problems = []
    z = zero_state(m)
    recs = m['records']
    if m.get('rule') != ZERO_RULE or z.get('rule') != ZERO_RULE or z.get('nexus') != 'Z0' or m.get('version') != 1:
        problems.append('the rule text, the zero gate name or the file version was changed')
    runs = m.get('runs')
    if not whole_number(runs) or runs < 0:
        return problems + ['the run counter is not a whole number']
    for k, v in z.items():
        if k in ('rule', 'nexus'):
            continue
        if k == 'operations':
            if not isinstance(v, dict) or not all(whole_number(x) and x >= 0 for x in v.values()):
                problems.append('the zero gate operation counts are damaged')
        elif not whole_number(v) or v < 0:
            problems.append('the zero gate counter %s is damaged' % k)
    if problems:
        return problems
    clock = m.get('clock')
    sessions = clock.get('sessions') if isinstance(clock, dict) else None
    if not whole_number(sessions) or sessions < 0:
        problems.append('the session counter is damaged')
        sessions = None
    # every record, in the order the gate stamped it
    ordered = sorted(((r['gid'], fam, r) for fam, key in FAMILIES for r in m[key] if whole_number(r.get('gid'))),
                     key=lambda x: x[0])
    last_run, last_t = 0, None
    updates = 0
    for gid, fam, r in ordered:
        run = r.get('run')
        if not whole_number(run) or run < 1 or run > runs + 1 or run < last_run:
            problems.append('%s record %s: its run number %r is out of order' % (fam, r.get('id'), run))
        else:
            last_run = run
        t = r.get('t')
        if t is not None:
            if not isinstance(t, list) or len(t) != 5 or not all(whole_number(x) and x >= 0 for x in t) \
                    or t[0] > z['passages'] or (sessions is not None and not 1 <= t[1] <= sessions):
                problems.append('%s record %s: its clock stamp is damaged or impossible' % (fam, r.get('id')))
            elif last_t is not None and (t[0] < last_t[0] or t[1] < last_t[1]
                                         or (t[1] == last_t[1] and (t[3] < last_t[3] or t[4] < last_t[4]))):
                problems.append('%s record %s: its clock stamp runs backwards' % (fam, r.get('id')))
            else:
                last_t = t
        for u in r.get('z0u', []):
            updates += 1
            if not isinstance(u, list) or len(u) < 2 or not whole_number(u[0]) or not 1 <= u[0] <= z['passages']:
                problems.append('%s record %s: a status change stamp is damaged' % (fam, r.get('id')))
        if r.get('z0u') and r['z0u'][-1][1:2] != [r.get('status')]:
            problems.append('%s record %s: its last status change does not match its status' % (fam, r.get('id')))
        if len(problems) >= 20:
            return problems + ['... more problems not listed']
    for fam, key in FAMILIES:               # Z0 passage numbers inside one archive count up without gaps
        last = 0
        for r in m[key]:
            if 'z0_late' in r:
                continue
            if not whole_number(r.get('z0')) or r['z0'] <= last or r['z0'] > z[fam + '_passages']:
                problems.append('%s record %s: its Z0 passage number is out of order' % (fam, r.get('id')))
                break
            last = r['z0']
    for w in m['wanted']:                   # asks: one for the first time, one more for each stamped change except the finding
        if w.get('asks') != 1 + len(w.get('z0u', [])) - (1 if w.get('status') == 'found' else 0):
            problems.append('want %s: the number of times it was asked (%r) does not match its stamped history' % (w.get('id'), w.get('asks')))
            break
    if z.get('updates', 0) != updates:
        problems.append('the gate counted %d status changes but the records show %d' % (z.get('updates', 0), updates))
    total = sum(z['operations'].values()) + z.get('updates', 0) + sum(z[fam + '_passages'] for fam, _k in FAMILIES)
    if z['passages'] != total:
        problems.append('the gate counted %d passages but its parts add up to %d' % (z['passages'], total))
    # search bounds saved in records
    for key, fields in (('punknowns', ('xp',)), ('proofs', ('pb', 'xb'))):
        for r in m[key]:
            for fld in fields:
                if fld in r and (not whole_number(r[fld]) or not 1 <= r[fld] <= 10 ** 6):
                    problems.append('%s %s: its saved search bound %s is damaged' % (key, r.get('id'), fld))
    # cursors
    own = {'pairs': None, 'mpairs': None, 'dpairs': None, 'xpairs': None, 'ppairs': None}
    sizes = {'pairs': len(recs), 'mpairs': len(recs), 'dpairs': len(recs), 'xpairs': len(recs), 'ppairs': len(m['planes'])}
    for name in own:
        bad, idx = cursor_problems(m.get(name), name, sizes[name])
        problems += bad
        own[name] = idx
    auto = lambda key: sum(1 for r in m[key] if not r.get('manual'))
    problems += pair_cursor_problems(m, own['pairs'])
    for name, key, per in (('mpairs', 'products', 2), ('dpairs', 'divisions', 1), ('xpairs', 'unknowns', 1), ('ppairs', 'punknowns', 1)):
        if own[name] is not None and own[name] * per != auto(key):
            problems.append('the %s cursor says %d pairs were done but the saved records show %d'
                            % (name, own[name], auto(key) // per))
    for name in ('slot_cursor', 'slot_pcursor'):
        c = m.get(name)
        if not isinstance(c, list) or len(c) != 2 or not all(whole_number(v) and v >= 0 for v in c) or c[1] > c[0] + 1:
            problems.append('the %s is damaged' % name)
    if not whole_number(m.get('slot_ref_rec')) or not 0 <= m['slot_ref_rec'] <= len(recs) \
            or not whole_number(m.get('slot_ref_pl')) or not 0 <= m['slot_ref_pl'] <= len(m['planes']):
        problems.append('the template cursors are damaged')
    else:
        refs, have = [SLOT_TEMPLATE], {SLOT_TEMPLATE}
        for r in recs[:m['slot_ref_rec']]:
            ref = str(r['value'])
            if ref not in have:
                refs.append(ref)
                have.add(ref)
        prefs = []
        for p in m['planes'][:m['slot_ref_pl']]:
            if p['p'][1] != 0:
                ref = '%di%d' % (abs(p['p'][0]), abs(p['p'][1]))
                if ref not in have:
                    prefs.append(ref)
                    have.add(ref)
        if m['slot_refs'] != refs or m['slot_prefs'] != prefs:
            problems.append('the template lists are not what the counter and the plane give')
    for key, st in m['slots'].items():
        symbols = breakdown(st.get('ref', ''))
        if st.get('symbols') != symbols or st.get('total') != len(SLOT_OPS) ** (len(symbols) - 1) \
                or key != st['ref'] + '|' + SLOT_SIG:
            problems.append('template %s: its saved shape does not match its name' % st.get('ref'))
    return problems[:20]


PRODUCT_WHY = {'multiply': 'adding a again and again, b times, from nothing',
               'rotate': 'turning every unit of a, b times, changed the number'}
DIVISION_WHY = {'divide': 'a 0 was put in to split the units into groups',
                'remainder': 'units were left over after the last full group'}
FRACTION_WHY = {'fraction': 'units left over after the last full group are a part of a group',
                'reduce': 'the leftover and the group can be split by the same g, and the part stays the same'}


def replay_roles(m):
    """Every role: a known name, its own place in the list, the reason it was given, and a record that
    really shows it (the test it was granted under is run again on that record)."""
    problems = []
    recs, prods, divs, fracs = m['records'], m['products'], m['divisions'], m['fractions']
    allowed = allowed_role_names()
    first_frac = {'fraction': 0, 'reduce': next((f['id'] for f in fracs if f['g'] >= 2), None)}
    first_div = {'divide': next((d['id'] for d in divs if d['status'] == 'done' and d['zeros'] >= 1), None),
                 'remainder': next((d['id'] for d in divs if d['status'] == 'done' and d['rem'] >= 1), None)}
    why_by_kind = {'unknown': UNKNOWN_WHY, 'plane': PLANE_WHY, 'punknown': PUNKNOWN_WHY, 'proof': PROOF_WHY,
                   'product': PRODUCT_WHY, 'division': DIVISION_WHY, 'fraction': FRACTION_WHY, 'approach': LIMIT_WHYS, 'difference': DIFF_WHYS, 'total': GROUP_WHYS}
    node_why = {n: w for n, _t, w in TURN_ROLES}
    names = set()
    for k, r in enumerate(m['roles']):
        name, ev, kind = r.get('name'), r.get('evidence'), r.get('kind')
        if r.get('id') != k:
            problems.append('role at position %d carries id %r' % (k, r.get('id')))
        if name not in allowed:
            problems.append('role %r is not a role the engine can grant' % (name,))
            continue
        if name in names:
            problems.append('role %s appears twice' % name)
        names.add(name)
        if r.get('given'):
            continue
        try:
            if kind == 'node':
                if r.get('why') != node_why.get(name) or r.get('rule') != TURN_ROLE_RULE:
                    problems.append('role %s: its reason or rule was changed' % name)
            elif kind in why_by_kind and r.get('why') != why_by_kind[kind].get(name):
                problems.append('role %s: its reason was changed' % name)
            if kind == 'product':
                p = prods[ev]
                base, count = recs[p['l']]['value'], recs[p['r']]['value']
                if name == 'multiply':
                    ok = p['kind'] == 'multiply' and p['status'] == 'done' and count >= 2
                else:
                    ok = p['kind'] == 'rotate' and p['v'] != [base, 0]
                if not ok:
                    problems.append('role %s: the product it points at does not show it' % name)
            elif kind == 'division':
                d = divs[ev]
                if d['status'] != 'done' or ev != first_div.get(name):
                    problems.append('role %s: it does not point at the first division that shows it' % name)
            elif kind == 'fraction':
                if ev != first_frac.get(name):
                    problems.append('role %s: it does not point at the first leftover that shows it' % name)
            elif kind == 'total':
                first = next((t['id'] for t in m['totals'] if t['before'] >= 1), None)
                if ev != first or r.get('rule') != GROUP_ROLE_RULE:
                    problems.append('role %s: it does not point at the first part stacked onto a whole that held parts, or its rule was changed' % name)
            elif kind == 'difference':
                first = next((d['id'] for d in m['differences'] if d['steps'] >= 1), None)
                if ev != first or r.get('rule') != DIFF_ROLE_RULE:
                    problems.append('role %s: it does not point at the first change that is more than nothing, or its rule was changed' % name)
            elif kind == 'approach':
                if ev != 0 or not m['approaches'] or r.get('rule') != LIMIT_ROLE_RULE:
                    problems.append('role %s: it does not point at the first approach, or its rule was changed' % name)
        except (KeyError, IndexError, TypeError):
            problems.append('role %s points at a record that does not show it' % name)
        if len(problems) >= 20:
            return problems + ['... more problems not listed']
    if any(t['before'] >= 1 for t in m['totals']) and 'group' not in names:
        problems.append('parts are stacked but the role group was never written down')
    if any(d['steps'] >= 1 for d in m['differences']) and 'difference' not in names:
        problems.append('changes are kept but the role difference was never written down')
    if m['approaches'] and 'limit' not in names:
        problems.append('approaches are kept but the role limit was never written down')
    return problems


# ---------------- deadlocks: a way back that ends in a move the engine blocks ----------------
# Going backwards (undo, which is untouched) can land on a move the engine's own rules block: a group of no
# units can never fill, so 0/x and x/0 cannot continue. That is a DEADLOCK, not an answer and not nothing.
# The path back is kept as it was, and the deadlock is kept in its own library, through Z0, for later use.

DEADLOCK_WORK_PER_RUN = 500      # blank searches looked at for deadlocks each run (phone-safety only)
DEADLOCK_WHY = 'the way back lands on a move the engine blocks (dividing by nothing), so the path cannot continue'


def deadlock_hit(m, kind, u, f, gate=False):
    """Does the way back for this form land on a move the engine itself blocks? Uses the engine's own sum."""
    if f.get('back') is None:
        return False
    if kind == 'unknown':
        a, x = m['records'][u['l']]['value'], f['back']
        A, B = ((a, 1), (x, 1)) if f['side'] == 'R' else ((x, 1), (a, 1))
        name, args = 'rational', (f['op'], A, B, u['limit'])
    else:
        a, x = tuple(m['planes'][u['l']]['p']), tuple(f['back'])
        A, B = (a, x) if f['side'] == 'R' else (x, a)
        name, args = 'cplx', (f['op'], A, B, u['limit'])
    res = zero_gate(m, 'operation', name=name, args=args) if gate else PRIMITIVES[name](*args)
    return res == 'DIV0'


def deadlock_text(m, kind, u, f):
    if kind == 'unknown':
        a, c, x = m['records'][u['l']]['value'], m['records'][u['r']]['value'], f['back']
        left = '%d%sx' % (a, f['op']) if f['side'] == 'R' else 'x%s%d' % (f['op'], a)
        return 'blank #%d, %s = %d: going backwards reaches %d, a move the engine blocks' % (u['id'], left, c, x)
    a, c, x = tuple(m['planes'][u['l']]['p']), tuple(m['planes'][u['r']]['p']), tuple(f['back'])
    left = '%s%sx' % (value_text(a), f['op']) if f['side'] == 'R' else 'x%s%s' % (f['op'], value_text(a))
    return 'plane blank #%d, %s = %s: going backwards reaches %s, a move the engine blocks' % (
        u['id'], left, value_text(c), value_text(x))


def deadlock_source(m, r):
    key = 'unknowns' if r['src'] == 'unknown' else 'punknowns'
    u = m[key][r['u']]
    return u, u['forms'][r['form']]


def deadlock_recipe(m, r):
    u, f = deadlock_source(m, r)
    if r['src'] == 'unknown':
        base = recipe_unknown(f['op'], f['side'], m['records'][u['l']]['value'], m['records'][u['r']]['value'], f['back'])
    else:
        base = recipe_punknown(m, f['op'], f['side'], tuple(m['planes'][u['l']]['p']),
                               tuple(m['planes'][u['r']]['p']), tuple(f['back']))
    return 'D ' + base


def add_deadlock(m, kind, u, fi):
    f = u['forms'][fi]
    rec = {'id': len(m['deadlocks']), 'src': kind, 'u': u['id'], 'form': fi, 'sum': f['op'], 'side': f['side'],
           'back': f['back'], 'why': DEADLOCK_WHY, 'op': 'deadlock', 'text': deadlock_text(m, kind, u, f),
           'watch': zero_split_watch(deadlock_dividend(m, kind, u, f), DEADLOCK_WATCH)}
    rec['recipe'] = deadlock_recipe(m, rec)
    zero_gate(m, 'record', record=rec, family='deadlock')
    m['deadlocks'].append(rec)
    return rec


def do_deadlocks(m, budget):
    """Look at every blank search in order. Where a way back ends in a blocked move, keep it as a deadlock.
    The cursor says how many blank searches have been looked at, so an older archive fills in over a few runs."""
    cur, made, looked = m['dl_cursor'], 0, 0
    seen = {(r['src'], r['u'], r['form']) for r in m['deadlocks']}
    for kind, key, c in (('unknown', 'unknowns', 'u'), ('punknown', 'punknowns', 'p')):
        while cur[c] < len(m[key]) and looked < budget and not STOP['flag']:
            u = m[key][cur[c]]
            for fi, f in enumerate(u['forms']):
                if (kind, u['id'], fi) not in seen and deadlock_hit(m, kind, u, f, gate=True):
                    add_deadlock(m, kind, u, fi)
                    made += 1
            cur[c] += 1
            looked += 1
    return made


def deadlock_status(m):
    cur = m['dl_cursor']
    return '  Deadlocks: %d kept (ways back that ended in a blocked move) | looked at %d of %d blanks, %d of %d plane blanks' % (
        len(m['deadlocks']), cur['u'], len(m['unknowns']), cur['p'], len(m['punknowns']))


def deadlock_line(r):
    w = r.get('watch')
    seen = '' if not w else '   watched %d steps: %d empty groups made, never closed' % (w['steps'], w['groups']) \
        if not w['ended'] else '   watched: closed after %d groups' % w['groups']
    return '#%d  %s%s   recipe: %s' % (r['id'], r['text'], seen, r['recipe'])


def upgrade_old(m):
    """A file saved before the deadlock library existed: add the empty library, once. Nothing else changes.
    A file that already has the library's counter is never touched, so a deleted library is not hidden."""
    if isinstance(m, dict) and isinstance(m.get('zero'), dict) and 'deadlock_passages' not in m['zero']:
        m['zero']['deadlock_passages'] = 0
        m.setdefault('deadlocks', [])
        m.setdefault('dl_cursor', {'u': 0, 'p': 0})
        return True
    return False


def replay_deadlocks(m):
    """Every deadlock is found again from the blank searches the cursor says were looked at, and no blocked
    way back below the cursor may be missing."""
    problems = []
    dl, cur, z = m['deadlocks'], m['dl_cursor'], zero_state(m)
    if not isinstance(cur, dict) or set(cur) != {'u', 'p'} or not all(whole_number(v) and v >= 0 for v in cur.values()) \
            or cur['u'] > len(m['unknowns']) or cur['p'] > len(m['punknowns']):
        return ['the deadlock cursor is damaged']
    expected = {}
    for kind, key, c in (('unknown', 'unknowns', 'u'), ('punknown', 'punknowns', 'p')):
        for uid in range(cur[c]):
            u = m[key][uid]
            for fi, f in enumerate(u['forms']):
                if deadlock_hit(m, kind, u, f):
                    expected[(kind, uid, fi)] = (u, f)
    got = {}
    for k, r in enumerate(dl):
        key = (r.get('src'), r.get('u'), r.get('form'))
        if r.get('id') != k or key in got:
            problems.append('deadlock %d is out of order or repeated' % k)
            break
        got[key] = r
        if key not in expected:
            problems.append('deadlock %d: that way back does not end in a blocked move' % k)
            continue
        u, f = expected[key]
        if (r.get('sum'), r.get('side'), r.get('back')) != (f['op'], f['side'], f['back']) or r.get('why') != DEADLOCK_WHY \
                or r.get('op') != 'deadlock' or r.get('text') != deadlock_text(m, key[0], u, f):
            problems.append('deadlock %d was edited: it does not match the blank search it came from' % k)
        w = r.get('watch')
        if not isinstance(w, dict) or not whole_number(w.get('steps')) or not 1 <= w['steps'] <= 10 ** 6 \
                or w != zero_split_watch(deadlock_dividend(m, key[0], u, f), w['steps']):
            problems.append('deadlock %d: its watch of the zero split is missing or does not come out the same' % k)
        if 'z0' not in r:
            problems.append('deadlock %d never passed through Z0' % k)
        if len(problems) >= 20:
            return problems + ['... more problems not listed']
    gone = sum(1 for key in expected if key not in got)
    if gone:
        problems.append('%d blocked ways back are missing from the deadlock library' % gone)
    for src in ('unknown', 'punknown'):
        seq = [(r['u'], r['form']) for r in dl if r.get('src') == src]
        if seq != sorted(seq):
            problems.append('the %s deadlocks are out of order' % src)
    st_ = [r['z0'] for r in dl if 'z0' in r]
    if len(set(st_)) != len(st_) or z['deadlock_passages'] != len(dl):
        problems.append('Z0 passage numbers for deadlocks do not match')
    return problems


# ---------------- solve: finish the work already in hand ----------------
# No new counter records and no new pairs. Only what the engine can already finish: parked items that the
# counter has grown past, fractions, plane points, proofs, deadlocks and wants that are behind.

SOLVE_ROUNDS = 20


def solve_tasks(m):
    names = ('pfreed', 'sfreed', 'fracs', 'points', 'proofs', 'deadlocks', 'tangents', 'approaches', 'differences', 'totals', 'wanted')
    total = dict.fromkeys(names, 0)
    begin_interrupt()
    try:
        for _ in range(SOLVE_ROUNDS):
            got = {'pfreed': retry_products(m), 'sfreed': retry_slots(m),
                   'fracs': do_fractions(m, FRAC_WORK_PER_RUN), 'points': scan_plane(m, PLANE_WORK_PER_RUN),
                   'proofs': 0 if slots_waiting(m) else run_proofs(m, PROOF_WORK_PER_RUN),
                   'deadlocks': do_deadlocks(m, DEADLOCK_WORK_PER_RUN),
                   'tangents': do_tangents(m, TANGENT_WORK_PER_RUN), 'approaches': do_approaches(m, APPROACH_WORK_PER_RUN), 'differences': do_differences(m, DIFFERENCE_WORK_PER_RUN), 'totals': do_totals(m, TOTAL_WORK_PER_RUN),
                   'wanted': resolve_wanted(m)}
            for k, v in got.items():
                total[k] += v
            if STOP['flag'] or not any(got.values()):
                break
    except KeyboardInterrupt:
        print('\nStopped hard in the middle of a step. The state is checked before anything is saved.')
    finally:
        end_interrupt()
    m['runs'] += 1
    zero_repair(m)
    problems = replay_light(m)
    if problems:
        print('\nSolve done but NOT saved: the archive fails its own replay, so the files on disk are untouched.')
    else:
        verified(m)
        save_memory(m)
        print('\nSolve done and saved. No new counter records and no new pairs were made.')
    print('  Freed: %d parked products, %d parked slot fillings | %d wants answered' % (total['pfreed'], total['sfreed'], total['wanted']))
    print('  Caught up: %d fractions, %d plane points, %d proofs, %d deadlocks, %d tangents, %d approaches, %d differences, %d totals' % (total['fracs'], total['points'], total['proofs'], total['deadlocks'], total['tangents'], total['approaches'], total['differences'], total['totals']))
    log = m['slot_log']
    behind = {'divisions not yet looked at for leftovers': len(m['divisions']) - m['fcursor'],
              'path nodes not yet looked at for plane points': len(m['nodes']) - m['plane_cur'],
              'slot fillings without a proof yet': max(0, len(log) - m['proof_cur'][0]),
              'walked pairs not yet looked at for tangents': len(m['expressions']) - m['tg_cursor'],
              'blank searches not yet checked for deadlocks': len(m['unknowns']) - m['dl_cursor']['u'] + len(m['punknowns']) - m['dl_cursor']['p']}
    waiting = {'parked products (need the counter to grow)': len(m['mul_parked']),
               'parked slot fillings (need the counter to grow)': len(m['slot_parked']),
               'wants still open': sum(1 for w in m['wanted'] if w['status'] == 'open')}
    still = [(k, v) for k, v in list(behind.items()) + list(waiting.items()) if v]
    if still:
        print('  Still waiting: ' + ' | '.join('%d %s' % (v, k) for k, v in still))
    else:
        print('  Nothing is left waiting.')
    replay_report(m, problems)


# ---------------- the zero split, watched ----------------
# A group of no units takes nothing, so the units left never fall below the group size and the split never
# closes. The engine refuses to start that loop (division_by_zero). The watch runs it for a fixed number of
# steps, records what it saw, and stops. Every deadlock keeps the watch with it.

DEADLOCK_WATCH = 5000        # steps the zero split is watched for


def zero_split_watch(left, steps):
    groups, size, ended = 0, 0, False
    for _ in range(steps):
        if isinstance(left, int) and left < size:      # fewer units than a group needs: the split would close
            ended = True
            break
        groups = S(groups)                             # one more (empty) group, and the units are not used up
    return {'steps': steps, 'groups': groups, 'left': left, 'ended': ended}


def deadlock_dividend(m, kind, u, f):
    if kind == 'unknown':
        return f['back'] if f['side'] == 'L' else m['records'][u['l']]['value']
    return list(f['back']) if f['side'] == 'L' else list(m['planes'][u['l']]['p'])


def upgrade_watch(m):
    """Deadlocks made before the watch existed (v23.3) get their watch now, once, through Z0 as a stamped change.
    The watch is fully worked out from the deadlock, so nothing is lost and nothing is guessed."""
    n = 0
    for r in m.get('deadlocks', []):
        if 'watch' not in r:
            u, f = deadlock_source(m, r)
            r['watch'] = zero_split_watch(deadlock_dividend(m, r['src'], u, f), DEADLOCK_WATCH)
            zero_gate(m, 'update', record=r)
            n += 1
    if n:
        print('  %d deadlocks from before the zero-split watch were given their watch (a stamped change through Z0).' % n)
    return n


# ---------------- tangents: every branch off a main path ----------------
# A pair walks a main path: S steps from one counted number. At every point on it the walker can leave the path:
# turn (I) and step, or step back against a unit (cancel). Each way off the main path is a TANGENT. Where the
# branch ends is recorded with it, and is not what makes it a tangent. Each branch is kept once, through Z0.

TANGENT_WORK_PER_RUN = 2000      # walked pairs looked at for tangents each run (phone-safety only)


def branch_step(kind, p):
    """Leave the main path at the counted number p: turn then step ('turn'), or step against a unit ('back').
    Uses only the engine's own turn and unit step."""
    d = turn(0) if kind == 'turn' else turn(turn(0))
    c, cx = unit_step([p, 0, 0, 0], d)
    return node_value(c), bool(cx)


PRIMITIVES['branch'] = branch_step


def tangent_recipe(kind, p):
    return '%s %s S' % (recipe_counter(p), 'I' if kind == 'turn' else 'I*2')


def tangent_text(t):
    return '%s at %d: leaves the main path and lands on %s%s' % (
        t['kind'], t['p'], value_text(tuple(t['dest'])), ' (a unit cancelled to Z0)' if t['cx'] else '')


def add_tangent(m, kind, p, e, k):
    dest, cx = zero_gate(m, 'operation', name='branch', args=(kind, p))
    rec = {'id': len(m['tangents']), 'kind': kind, 'p': p, 'dest': list(dest), 'cx': cx,
           'expr': e['id'], 'step': k, 'op': 'tangent', 'recipe': tangent_recipe(kind, p)}
    zero_gate(m, 'record', record=rec, family='tangent')
    m['tangents'].append(rec)
    return rec


def do_tangents(m, budget):
    """Walk each walked pair's main path again, in order, and keep every branch off it that is not kept yet."""
    recs, made, looked = m['records'], 0, 0
    seen = {(t['kind'], t['p']) for t in m['tangents']}
    while m['tg_cursor'] < len(m['expressions']) and looked < budget and not STOP['flag']:
        e = m['expressions'][m['tg_cursor']]
        n, count = e['l'], recs[e['r']]['value']
        for k in range(count + 1):
            p = recs[n]['value']
            for kind in ('turn', 'back'):
                if (kind, p) not in seen:
                    seen.add((kind, p))
                    add_tangent(m, kind, p, e, k)
                    made += 1
            if k < count:
                n = recs[n]['nxt']
        m['tg_cursor'] += 1
        looked += 1
    return made


def tangent_class(m, t):
    d = tuple(t['dest'])
    if d == (0, 0):
        return 'back at Z0'
    if d in plane_seen(m):
        return 'a point already in the plane library'
    return 'a point not reached yet'


def tangent_line(m, t):
    return '#%d  %s  [%s]  first seen on walked pair #%d, step %d   recipe: %s' % (
        t['id'], tangent_text(t), tangent_class(m, t), t['expr'], t['step'], t['recipe'])


def tangent_status(m):
    return '  Tangents: %d branches off main paths kept | looked at %d of %d walked pairs%s' % (
        len(m['tangents']), m['tg_cursor'], len(m['expressions']),
        ' | pair exploration PAUSED: waiting for something new' if pair_paused(m) else '')


def upgrade_tangents(m):
    """A file saved before the tangent library existed: add the empty library, once."""
    if isinstance(m, dict) and isinstance(m.get('zero'), dict) and 'tangent_passages' not in m['zero']:
        m['zero']['tangent_passages'] = 0
        m.setdefault('tangents', [])
        m.setdefault('tg_cursor', 0)
        m.setdefault('pair_pause', {'sig': None})
        return True
    return False


def replay_tangents(m):
    """Every branch is found again from the walked pairs the cursor says were looked at, in the same order."""
    problems = []
    tg, z, cur = m['tangents'], zero_state(m), m['tg_cursor']
    if not whole_number(cur) or not 0 <= cur <= len(m['expressions']):
        return ['the tangent cursor is damaged']
    recs, expect, seen = m['records'], [], set()
    for e in m['expressions'][:cur]:
        n, count = e['l'], recs[e['r']]['value']
        for k in range(count + 1):
            p = recs[n]['value']
            for kind in ('turn', 'back'):
                if (kind, p) not in seen:
                    seen.add((kind, p))
                    expect.append((kind, p, e['id'], k))
            if k < count:
                n = recs[n]['nxt']
    if len(tg) != len(expect):
        problems.append('the tangent library holds %d branches but the walked pairs give %d' % (len(tg), len(expect)))
    for i, (t, (kind, p, eid, k)) in enumerate(zip(tg, expect)):
        dest, cx = branch_step(kind, p)
        if (t.get('id'), t.get('kind'), t.get('p'), t.get('expr'), t.get('step'), t.get('dest'), t.get('cx'),
                t.get('op'), t.get('recipe')) != (i, kind, p, eid, k, list(dest), cx, 'tangent', tangent_recipe(kind, p)):
            problems.append('tangent %d does not match the walked pair it came from' % i)
        if 'z0' not in t:
            problems.append('tangent %d never passed through Z0' % i)
        if len(problems) >= 20:
            return problems + ['... more problems not listed']
    st_ = [t['z0'] for t in tg if 'z0' in t]
    if len(set(st_)) != len(st_) or z['tangent_passages'] != len(tg):
        problems.append('Z0 passage numbers for tangents do not match')
    if z['operations'].get('branch', 0) < len(tg):
        problems.append('Z0 saw %d branch steps but there are %d tangents' % (z['operations'].get('branch', 0), len(tg)))
    pp = m.get('pair_pause')
    if not isinstance(pp, dict) or set(pp) != {'sig'}:
        problems.append('the pair pause is damaged')
    elif pp['sig'] is not None:
        sig = pp['sig']
        if not isinstance(sig, list) or len(sig) != 4 or not all(whole_number(v) and v >= 0 for v in sig) \
                or not any(tuple(w['key']) == ('pause',) + tuple(sig) for w in m['wanted']):
            problems.append('the pair pause is set but the wanted archive does not hold what it waits for')
    return problems


# ---------------- approaches: paths that close in without arriving (v23.14) ----------------
# A path can fail to close in two ways. It can be STUCK (dividing by nothing goes nowhere: a deadlock), or it can
# CLOSE IN: 1/1, 1/2, 1/3, 1/4 ... each step lands nearer to 0 and none ever arrives. The deadlocks keep the first
# kind. This library keeps the second, apart from them, through Z0.
# The paths are the splits the engine already made: for one counted number a, the divisions a/1, a/2, a/3 ...
# in order, with no divisor missing. The gap at each step is a/b minus the target, kept as an exact fraction.
# The test lets the gap wobble. The path closes in when
#   - there are at least three steps and no gap is zero or below (the target is never reached or crossed),
#   - the best gap so far improves at least twice, and
#   - the last gap is smaller than every gap before it.
# The target is the lowest value the engine holds. Each path is kept once, at the length it had when it first
# passed. The comparing of sizes is only a look at records already made: it makes no new value.

APPROACH_WORK_PER_RUN = 300      # groups of divisions looked at each run (phone-safety only)
APPROACH_WHY = 'the gap to the target gets smaller and the last step is the nearest yet, and no step reaches or crosses the target'


def approach_gaps(a, t, bs):
    """The gap a/b - t at every step, as exact [top, bottom] pairs."""
    return [[a - t * b, b] for b in bs]


def gap_less(g, h):
    return g[0] * h[1] < h[0] * g[1]


def closing_in(gaps):
    if len(gaps) < 3 or any(g[0] <= 0 for g in gaps):
        return False
    best, better = gaps[0], 0
    for g in gaps[1:]:
        if gap_less(g, best):
            best, better = g, better + 1
    last = gaps[-1]
    return better >= 2 and gap_less(last, gaps[0]) and all(gap_less(last, g) for g in gaps[:-1])


def approach_test(a, t, bs):
    gaps = approach_gaps(a, t, list(bs))
    return closing_in(gaps), gaps


PRIMITIVES['approach_test'] = approach_test


def approach_target(m):
    """The lowest value the engine holds: record 0, which is Z0."""
    return m['records'][0]['value'], 0


def approach_groups(m):
    """For each counted number a, the divisions a/b that finished, by divisor, with no divisor missing."""
    recs, groups = m['records'], {}
    for d in m['divisions']:
        if d.get('status') != 'done':
            continue
        a, b = recs[d['l']]['value'], recs[d['r']]['value']
        if b >= 1:
            groups.setdefault(a, {}).setdefault(b, d['id'])
    out = []
    for a in sorted(groups):
        items = sorted(groups[a].items())
        run = [items[0]]
        for item in items[1:]:
            if item[0] != run[-1][0] + 1:
                break
            run.append(item)
        out.append((a, run))
    return out


def approach_recipe(m, r):
    recs, divs = m['records'], m['divisions']
    first, last = divs[r['divs'][0]], divs[r['divs'][-1]]
    a = recs[first['l']]['value']
    return 'A ' + recipe_divide(a, recs[first['r']]['value']) + ' .. ' + recipe_divide(a, recs[last['r']]['value']) + ' > ' + recipe_counter(r['target'])


def approach_text(m, r):
    recs, divs = m['records'], m['divisions']
    b1, bn = recs[divs[r['divs'][0]]['r']]['value'], recs[divs[r['divs'][-1]]['r']]['value']
    return '%d / %d, %d / %d ... %d / %d: the gap to %d gets smaller (%d steps) and never reaches it' % (
        r['a'], b1, r['a'], b1 + 1, r['a'], bn, r['target'], r['terms'])


def add_approach(m, a, run, t, gaps):
    rec = {'id': len(m['approaches']), 'a': a, 'divs': [did for _, did in run], 'target': t, 'tid': 0, 'gaps': gaps,
           'terms': len(run), 'why': APPROACH_WHY, 'op': 'approach'}
    rec['text'] = approach_text(m, rec)
    rec['recipe'] = approach_recipe(m, rec)
    zero_gate(m, 'record', record=rec, family='approach')
    m['approaches'].append(rec)
    return rec


LIMIT_ROLE_RULE = 'first_path_that_closes_in_v1'
LIMIT_WHY = 'a path closes in on a value and never arrives: each step is nearer than any before'
LIMIT_WHYS = {'limit': LIMIT_WHY}


def limit_role(m):
    """The first approach kept is the evidence for the role limit. Written once, never again."""
    if m['approaches'] and find_role(m, 'limit') is None:
        first = m['approaches'][0]
        add_role(m, 'limit', LIMIT_ROLE_RULE, kind='approach', evidence=first['id'], why=LIMIT_WHY,
                 recipe=approach_recipe(m, first))
        return True
    return False


def do_approaches(m, budget):
    """Look at the groups of divisions in turn. A group that closes in on the target and is not kept yet is kept."""
    groups = approach_groups(m)
    if not groups:
        limit_role(m)
        return 0
    have = {r['a'] for r in m['approaches']}
    t, _ = approach_target(m)
    start, made, looked = m['ap_cursor'] % len(groups), 0, 0
    while looked < min(budget, len(groups)) and not STOP['flag']:
        a, run = groups[(start + looked) % len(groups)]
        looked += 1
        if a in have or len(run) < 3:
            continue
        ok, gaps = zero_gate(m, 'operation', name='approach_test', args=(a, t, tuple(b for b, _ in run)))
        if ok:
            add_approach(m, a, run, t, gaps)
            have.add(a)
            made += 1
    m['ap_cursor'] = (start + looked) % len(groups)
    limit_role(m)
    return made


def approach_line(m, r):
    return '#%d  %s   recipe: %s' % (r['id'], r['text'], r['recipe'])


def approach_status(m):
    groups = approach_groups(m)
    return '  Approaches: %d paths that close in on a value without arriving kept | %d groups of divisions with 3 or more steps | stuck paths stay in the deadlocks' % (
        len(m['approaches']), sum(1 for _, run in groups if len(run) >= 3))


def upgrade_approaches(m):
    """A file saved before the approaches library existed: add the empty library, once."""
    if isinstance(m, dict) and isinstance(m.get('zero'), dict) and 'approach_passages' not in m['zero']:
        m['zero']['approach_passages'] = 0
        m.setdefault('approaches', [])
        m.setdefault('ap_cursor', 0)
        return True
    return False


def replay_approaches(m):
    """Every approach is worked out again from the divisions it names. Nothing is trusted from the stored gaps."""
    problems = []
    ap, z, recs, divs = m['approaches'], zero_state(m), m['records'], m['divisions']
    if not whole_number(m['ap_cursor']) or m['ap_cursor'] < 0:
        return ['the approaches cursor is damaged']
    seen = set()
    for k, r in enumerate(ap):
        if r.get('id') != k or r.get('a') in seen:
            problems.append('approach %d is out of order or repeated' % k)
            break
        seen.add(r.get('a'))
        ds = r.get('divs')
        if not isinstance(ds, list) or len(ds) < 3 or not all(ref_ok(x, len(divs)) for x in ds) or r.get('terms') != len(ds):
            problems.append('approach %d: the divisions it names are damaged' % k)
            continue
        a, bs, fine = r.get('a'), [], True
        for x in ds:
            d = divs[x]
            if d.get('status') != 'done' or recs[d['l']]['value'] != a:
                fine = False
                break
            bs.append(recs[d['r']]['value'])
        if not fine or bs[0] < 1 or any(bs[i + 1] != bs[i] + 1 for i in range(len(bs) - 1)):
            problems.append('approach %d: its divisions are not one counted number split by 1, 2, 3 ... in order' % k)
            continue
        t, tid = approach_target(m)[0], 0
        ok, gaps = approach_test(a, t, bs)
        if not ok or r.get('gaps') != gaps or r.get('target') != t or r.get('tid') != tid or r.get('why') != APPROACH_WHY \
                or r.get('op') != 'approach':
            problems.append('approach %d does not come out the same: it does not close in on its target, or it was edited' % k)
            continue
        if r.get('text') != approach_text(m, r):
            problems.append('approach %d: its text was edited' % k)
        if 'z0' not in r:
            problems.append('approach %d never passed through Z0' % k)
        if len(problems) >= 20:
            return problems + ['... more problems not listed']
    st_ = [r['z0'] for r in ap if 'z0' in r]
    if len(set(st_)) != len(st_) or z['approach_passages'] != len(ap):
        problems.append('Z0 passage numbers for approaches do not match')
    return problems


# ---------------- differences: the change between neighbours (v23.16) ----------------
# For one counted number a, the products a x b and a x (b+1) are neighbours: the count took one more step. The
# engine climbs from the smaller product to the larger with S alone and counts the steps. That count is the change.
# Where nothing changes (a is 0) the change is nothing, and it is kept too. Each change is kept once, through Z0.
# The first change that is more than nothing is the evidence for the role difference.

DIFFERENCE_WORK_PER_RUN = 200     # neighbouring pairs of products looked at each run (phone-safety only)
DIFF_ROLE_RULE = 'first_change_between_neighbours_v1'
DIFF_WHY = 'one more step in the count changes the product: the climb from one to the next took S steps'
DIFF_WHYS = {'difference': DIFF_WHY}


def climb(low, high):
    """Count the S steps it takes to get from low up to high."""
    n, x = 0, low
    while x < high:
        x = S(x)
        n += 1
    return n


PRIMITIVES['climb'] = climb


def difference_recipe(m, r):
    recs = m['records']
    a, b = recs[r['l']]['value'], recs[r['r']]['value']
    return 'N ' + recipe_multiply(a, b) + ' .. ' + recipe_multiply(a, b + 1) + ' S*%d' % r['steps']


def difference_text(m, r):
    recs = m['records']
    a, b = recs[r['l']]['value'], recs[r['r']]['value']
    return '%d x %d = %d and %d x %d = %d: one more step in the count changes the result by %d' % (
        a, b, r['from'], a, b + 1, r['to'], r['steps'])


def difference_role(m):
    """The first change that is more than nothing is the evidence for the role difference. Written once."""
    if find_role(m, 'difference') is None:
        first = next((d for d in m['differences'] if d['steps'] >= 1), None)
        if first is not None:
            add_role(m, 'difference', DIFF_ROLE_RULE, kind='difference', evidence=first['id'], why=DIFF_WHY,
                     recipe=difference_recipe(m, first))
            return True
    return False


def difference_pairs(m):
    """Every pair of neighbouring finished products (same a, b and b+1), in order of a then b."""
    done = {}
    for p in m['products']:
        if p.get('kind') == 'multiply' and p.get('status') == 'done' and p.get('v') is not None:
            done.setdefault((p['l'], p['r']), p['id'])
    return [(l, r, done[(l, r)], done[(l, r + 1)]) for (l, r) in sorted(done) if (l, r + 1) in done]


def do_differences(m, budget):
    have = {(d['l'], d['r']) for d in m['differences']}
    made = 0
    for l, r, p1, p2 in difference_pairs(m):
        if made >= budget or STOP['flag']:
            break
        if (l, r) in have:
            continue
        low, high = m['products'][p1]['v'][0], m['products'][p2]['v'][0]
        if high < low:
            continue
        steps = zero_gate(m, 'operation', name='climb', args=(low, high))
        rec = {'id': len(m['differences']), 'p1': p1, 'p2': p2, 'l': l, 'r': r, 'from': low, 'to': high,
               'steps': steps, 'op': 'difference'}
        rec['text'] = difference_text(m, rec)
        rec['recipe'] = difference_recipe(m, rec)
        zero_gate(m, 'record', record=rec, family='difference')
        m['differences'].append(rec)
        have.add((l, r))
        made += 1
    difference_role(m)
    return made


def difference_line(m, r):
    return '#%d  %s   recipe: %s' % (r['id'], r['text'], r['recipe'])


def difference_status(m):
    real = sum(1 for d in m['differences'] if d['steps'] >= 1)
    return '  Differences: %d changes between neighbouring products kept (%d more than nothing) | role: %s' % (
        len(m['differences']), real, 'found' if find_role(m, 'difference') else 'not found yet')


def upgrade_differences(m):
    """A file saved before the differences library existed: add the empty library, once."""
    if isinstance(m, dict) and isinstance(m.get('zero'), dict) and 'difference_passages' not in m['zero']:
        m['zero']['difference_passages'] = 0
        m.setdefault('differences', [])
        return True
    return False


def replay_differences(m):
    """Every change is climbed again with S alone, from the two products it names."""
    problems = []
    df, z, recs, prods = m['differences'], zero_state(m), m['records'], m['products']
    seen = set()
    for k, r in enumerate(df):
        key = (r.get('l'), r.get('r'))
        if r.get('id') != k or key in seen:
            problems.append('difference %d is out of order or repeated' % k)
            break
        seen.add(key)
        if not (ref_ok(r.get('p1'), len(prods)) and ref_ok(r.get('p2'), len(prods)) and ref_ok(r.get('l'), len(recs))
                and ref_ok(r.get('r'), len(recs))):
            problems.append('difference %d: the products it names are damaged' % k)
            continue
        p1, p2 = prods[r['p1']], prods[r['p2']]
        if p1.get('kind') != 'multiply' or p2.get('kind') != 'multiply' or p1.get('status') != 'done' or p2.get('status') != 'done' \
                or p1.get('l') != r['l'] or p2.get('l') != r['l'] or p1.get('r') != r['r'] or p2.get('r') != r['r'] + 1 \
                or p1.get('v') is None or p2.get('v') is None:
            problems.append('difference %d: they are not two neighbouring finished products of the same number' % k)
            continue
        low, high = p1['v'][0], p2['v'][0]
        if high < low or (r.get('from'), r.get('to')) != (low, high) or r.get('steps') != climb(low, high) or r.get('op') != 'difference':
            problems.append('difference %d does not come out the same when climbed again from S' % k)
            continue
        if r.get('text') != difference_text(m, r):
            problems.append('difference %d: its text was edited' % k)
        if 'z0' not in r:
            problems.append('difference %d never passed through Z0' % k)
        if len(problems) >= 20:
            return problems + ['... more problems not listed']
    st_ = [r['z0'] for r in df if 'z0' in r]
    if len(set(st_)) != len(st_) or z['difference_passages'] != len(df):
        problems.append('Z0 passage numbers for differences do not match')
    return problems


# ---------------- totals: smaller parts stacked onto a bigger whole (v23.17) ----------------
# The counted numbers 1, 2, 3 ... are the parts. The first part is stacked onto nothing. Every later part is stacked
# onto the whole that the parts before it made: the engine climbs from that whole with S, one step for each unit of the
# part. Each stack is kept once, through Z0, and is built on the one before it, so the whole grows part by part.
# The first time a part is stacked onto a whole that already holds parts, that record is the evidence for the role group.

TOTAL_WORK_PER_RUN = 50      # parts stacked each run (phone-safety only)
GROUP_ROLE_RULE = 'first_part_stacked_on_a_whole_v1'
GROUP_WHY = 'a part was stacked onto a whole that already held parts: smaller parts make a bigger whole'
GROUP_WHYS = {'group': GROUP_WHY}


def stack_up(whole, part):
    """Climb from the whole with S, one step for each unit of the part."""
    x = whole
    for _ in range(part):
        x = S(x)
    return x


PRIMITIVES['stack'] = stack_up


def total_recipe(m, r):
    return 'G ' + recipe_add(r['before'], m['records'][r['part']]['value'])


def total_text(m, r):
    return 'part %d stacked onto the whole of %d gives %d' % (m['records'][r['part']]['value'], r['before'], r['after'])


def group_role(m):
    if find_role(m, 'group') is None:
        first = next((t for t in m['totals'] if t['before'] >= 1), None)
        if first is not None:
            add_role(m, 'group', GROUP_ROLE_RULE, kind='total', evidence=first['id'], why=GROUP_WHY,
                     recipe=total_recipe(m, first))
            return True
    return False


def do_totals(m, budget):
    made = 0
    while made < budget and not STOP['flag'] and len(m['totals']) + 1 < len(m['records']):
        k = len(m['totals'])
        part = k + 1
        before = m['totals'][-1]['after'] if k else 0
        after = zero_gate(m, 'operation', name='stack', args=(before, m['records'][part]['value']))
        rec = {'id': k, 'part': part, 'before': before, 'after': after, 'op': 'total'}
        rec['text'] = total_text(m, rec)
        rec['recipe'] = total_recipe(m, rec)
        zero_gate(m, 'record', record=rec, family='total')
        m['totals'].append(rec)
        made += 1
    group_role(m)
    return made


def total_line(m, r):
    return '#%d  %s   recipe: %s' % (r['id'], r['text'], r['recipe'])


def total_status(m):
    last = m['totals'][-1] if m['totals'] else None
    return '  Totals: %d parts stacked onto the whole%s | role: %s' % (
        len(m['totals']), '' if last is None else ' (the whole is now %d)' % last['after'],
        'found' if find_role(m, 'group') else 'not found yet')


def upgrade_totals(m):
    """A file saved before the totals library existed: add the empty library, once."""
    if isinstance(m, dict) and isinstance(m.get('zero'), dict) and 'total_passages' not in m['zero']:
        m['zero']['total_passages'] = 0
        m.setdefault('totals', [])
        return True
    return False


def replay_totals(m):
    """Every stack is climbed again with S alone, and each one must be built on the one before it."""
    problems = []
    tt, z, recs = m['totals'], zero_state(m), m['records']
    before = 0
    for k, r in enumerate(tt):
        if r.get('id') != k or r.get('part') != k + 1 or not ref_ok(r.get('part'), len(recs)):
            problems.append('total %d is out of order or names the wrong part' % k)
            break
        if r.get('before') != before or r.get('op') != 'total':
            problems.append('total %d is not built on the one before it' % k)
            break
        after = stack_up(before, recs[r['part']]['value'])
        if r.get('after') != after:
            problems.append('total %d does not come out the same when climbed again from S' % k)
            break
        if r.get('text') != total_text(m, r):
            problems.append('total %d: its text was edited' % k)
        if 'z0' not in r:
            problems.append('total %d never passed through Z0' % k)
        before = after
        if len(problems) >= 20:
            return problems + ['... more problems not listed']
    st_ = [r['z0'] for r in tt if 'z0' in r]
    if len(set(st_)) != len(st_) or z['total_passages'] != len(tt):
        problems.append('Z0 passage numbers for totals do not match')
    return problems


# ---------------- the pair pause ----------------
# When a full pass over the walked pairs keeps no new branch, pair exploration stops and the engine saves.
# What it waits for is kept in the wanted archive (so it is stamped). Anything new restarts it: a new counter
# record, a typed pair, a typed equation.

def pause_sig(m):
    # typed equations count (manual); the blanks the engine tries by itself are not something new introduced
    return [len(m['records']), len(m['expressions']),
            sum(1 for u in m['unknowns'] if u.get('manual')), sum(1 for u in m['punknowns'] if u.get('manual'))]


def pair_paused(m):
    sig = m['pair_pause']['sig']
    return sig is not None and sig == pause_sig(m)


def settle_pair_pause(m, walked, tangled):
    if walked and not tangled and m['tg_cursor'] == len(m['expressions']):
        sig = pause_sig(m)
        m['pair_pause']['sig'] = sig
        want_check(m, ('pause',) + tuple(sig), False)
    elif tangled:
        m['pair_pause']['sig'] = None


# ---------------- typed pairs are marked, so the pair cursor can be checked exactly ----------------

def upgrade_pairs(m):
    """A file from before typed pairs were marked: remember where the pair cursor stood, once. From there on
    the cursor must equal that plus the pairs the engine walked itself."""
    if isinstance(m, dict) and isinstance(m.get('zero'), dict) and 'pair_marks' not in m['zero']:
        m['zero']['pair_marks'] = 1
        idx = 0
        try:
            c = m['pairs']
            idx = c['n'] * c['n'] + 2 * c['i'] + c['step']
        except (KeyError, TypeError):
            pass
        m['pair_base'] = {'n': len(m.get('expressions', [])), 'idx': idx}
        return True
    return False


def pair_cursor_problems(m, idx):
    """The pairs cursor against the walked pairs: exact from the point marking began."""
    base = m.get('pair_base')
    if not isinstance(base, dict) or set(base) != {'n', 'idx'} or not whole_number(base['n']) or not whole_number(base['idx']) \
            or not 0 <= base['n'] <= len(m['expressions']) or base['idx'] < 0:
        return ['the pair marking base is damaged']
    if idx is None:
        return []
    expect = base['idx'] + sum(1 for e in m['expressions'][base['n']:] if not e.get('manual'))
    if idx != expect:
        return ['the pair cursor says %d pairs were done but the saved walks show %d' % (idx, expect)]
    return []


# ---------------- v23.8: every change to a stored record is a new stamp ----------------
# The three cores that change a record without stamping it (step -> nxt, retry_slots -> limit and need,
# retry_products -> limit and tries) are NOT edited. Each is wrapped: the wrapper keeps the old values,
# calls the core exactly as it is, then stamps whatever changed through Z0. The change rides inside the
# stamp, so the replay can check the record's final values against its own stamped history.

_CORE_STEP, _CORE_RETRY_SLOTS, _CORE_RETRY_PRODUCTS = step, retry_slots, retry_products


def note_change(m, rec, old_len, details):
    """Make sure the record's newest Z0 stamp carries `details`. If the core already stamped it (a status
    change), the details join that stamp. Otherwise a new stamp is made first."""
    if len(rec.get('z0u', [])) == old_len:
        zero_gate(m, 'update', record=rec)
    rec['z0u'][-1].append(details)


def step_stamped(m):
    last = m['records'][-1]
    old = len(last.get('z0u', []))
    _CORE_STEP(m)
    note_change(m, last, old, {'nxt': last['nxt']})


def retry_slots_stamped(m):
    log = m['slot_log']
    before = {rid: (log[rid]['limit'], log[rid]['need'], len(log[rid].get('z0u', []))) for rid in m['slot_parked']}
    freed = _CORE_RETRY_SLOTS(m)
    for rid, (limit, need, n) in before.items():
        rec = log[rid]
        if (rec['limit'], rec['need']) != (limit, need):
            note_change(m, rec, n, {'limit': rec['limit'], 'need': rec['need'], 'try': len(stamp_details(rec)) + 1})
    return freed


def retry_products_stamped(m):
    prods = m['products']
    before = {rid: (prods[rid]['limit'], prods[rid]['tries'], len(prods[rid].get('z0u', []))) for rid in m['mul_parked']}
    freed = _CORE_RETRY_PRODUCTS(m)
    for rid, (limit, tries, n) in before.items():
        rec = prods[rid]
        if (rec['limit'], rec['tries']) != (limit, tries):
            note_change(m, rec, n, {'limit': rec['limit'], 'tries': rec['tries']})
    return freed


step, retry_slots, retry_products = step_stamped, retry_slots_stamped, retry_products_stamped


def upgrade_stamps(m):
    """A file from before change stamps: the counter records it already holds are exempt, from the newest one on
    every nxt link is stamped."""
    if isinstance(m, dict) and isinstance(m.get('zero'), dict) and 'change_stamps' not in m['zero']:
        m['zero']['change_stamps'] = 1
        m['stamp_base'] = {'nxt': max(0, len(m.get('records', [])) - 1), 'prod': len(m.get('products', [])),
                           'slot': len(m.get('slot_log', []))}
        return True
    if isinstance(m, dict) and isinstance(m.get('stamp_base'), dict) and set(m['stamp_base']) == {'nxt', 'prod'}:
        m['stamp_base']['slot'] = len(m.get('slot_log', []))       # a v23.8 file: slots it holds are exempt
        return True
    return False


def stamp_details(r):
    return [d for u in r.get('z0u', []) if isinstance(u, list) for d in u[2:] if isinstance(d, dict)]


def replay_stamps(m):
    """Every change to a stored record has its stamp, and the record's values agree with their stamped history."""
    problems = []
    recs = m['records']
    if m['zero'].get('change_stamps') != 1:
        return ['the change-stamp marker is missing']
    base = m.get('stamp_base')
    if not isinstance(base, dict) or set(base) != {'nxt', 'prod', 'slot'} or not all(whole_number(base[k]) for k in base) \
            or not 0 <= base['nxt'] <= max(len(recs) - 1, 0) or not 0 <= base['prod'] <= len(m['products']) \
            or not 0 <= base['slot'] <= len(m['slot_log']):
        return ['the change-stamp base is damaged']
    for i, r in enumerate(recs):
        det = stamp_details(r)
        if base['nxt'] <= i < len(recs) - 1:
            if det != [{'nxt': i + 1}]:
                problems.append('counter record %d: the change of its next link is not stamped exactly once' % i)
        elif det:
            problems.append('counter record %d has a change stamp it should not have' % i)
        if len(problems) >= 20:
            return problems + ['... more problems not listed']
    for key, fields, tick in (('slot_log', ('limit', 'need'), None), ('products', ('limit', 'tries'), 'tries')):
        for r in m[key]:
            det = stamp_details(r)
            if key == 'products' and 'tries' in r and r.get('id', 0) >= base['prod'] and r['tries'] != 1 + len(det):
                problems.append('products %s: it was tried %r times but %d changes are stamped' % (r.get('id'), r['tries'], len(det)))
            if not det:
                continue
            last = None
            for j, d in enumerate(det, 1):
                if key == 'slot_log':
                    if 'try' in d and d['try'] != j or 'try' not in d and r.get('id', 0) >= base['slot']:
                        problems.append('slot_log %s: its retry stamps are not counted 1, 2, 3 ... without a gap' % r.get('id'))
                        break
                    d = {k: v for k, v in d.items() if k != 'try'}
                if set(d) != set(fields) or not all(whole_number(d[f]) for f in fields):
                    problems.append('%s %s: a change stamp is damaged' % (key, r.get('id')))
                    break
                if last is not None and (d['limit'] <= last['limit'] or (tick and d[tick] != last[tick] + 1)):
                    problems.append('%s %s: its stamped changes do not follow on from each other' % (key, r.get('id')))
                    break
                last = d
            else:
                if any(r.get(f) != last[f] for f in fields):
                    problems.append('%s %s: its values do not match its last stamped change' % (key, r.get('id')))
            if len(problems) >= 20:
                return problems + ['... more problems not listed']
    for c in m['corrections']:
        det = stamp_details(c)
        if det and (len(det) != 1 or det[0] != {'who': c.get('who')} or not str(c.get('who')).startswith('Dragon Z v')):
            problems.append('correction %s has a change stamp that does not agree with its label' % c.get('id'))
    for fam, key in FAMILIES:
        if key in ('records', 'slot_log', 'products', 'corrections'):
            continue
        for r in m[key]:
            if stamp_details(r):
                problems.append('%s %s has a change stamp that no family writes' % (fam, r.get('id')))
                break
    return problems


# ---------------- v23.10: every inner step is counted, and handed to Z0 in batches (the phone version) ----------------
# S, unit_step, turn and turn_units are the single steps every composite operation is made of. Here each one is
# counted the moment it happens, with a cheap counter, and the counts are handed to Z0 in one batch before every
# check and save. Z0 ends up with exactly the numbers the NOT FOR PHONES file reaches (inner_S, inner_Sd, inner_I,
# inner_Iu), without a gate passage per step. The batch is added to Z0's counters by this code, not by zero_gate
# itself (zero_gate is a core and is not edited). No core is edited: the four names are rebound to counting copies.

GATE = {'m': None}          # the archive the counts belong to; None = nothing is counted (the replay, loading)
GATE_NOTE = 'PHONE VERSION: every inner step is counted as it happens and handed to Z0 in batches before each check and save.'
_COUNT = {'S': [0], 'Sd': [0], 'I': [0], 'Iu': [0]}
_RAW_STEPS = {'S': S, 'Sd': unit_step, 'I': turn, 'Iu': turn_units}
for _name, _raw in _RAW_STEPS.items():
    PRIMITIVES['inner_' + _name] = _raw


def _counted_step(name, raw):
    cell = _COUNT[name]

    def counted(*args):
        if GATE['m'] is not None:
            cell[0] += 1
        return raw(*args)
    return counted


S, unit_step, turn, turn_units = (_counted_step('S', S), _counted_step('Sd', unit_step), _counted_step('I', turn),
                                  _counted_step('Iu', turn_units))


def flush_inner(m=None):
    """Hand the counted inner steps to Z0: each one is a passage, added to its own count and to the gate's total."""
    m = GATE['m'] if m is None else m
    if m is None:
        return 0
    z = zero_state(m)
    total = 0
    for name, cell in _COUNT.items():
        n = cell[0]
        if n:
            key = 'inner_' + name
            z['operations'][key] = z['operations'].get(key, 0) + n
            z['passages'] += n
            cell[0] = 0
            total += n
    return total


def replay(m):
    """The independent check. The counted steps are handed to Z0 first, and the counting is off while it runs."""
    held = GATE['m']
    flush_inner()
    GATE['m'] = None
    try:
        return _replay_plain(m)
    finally:
        GATE['m'] = held


def _replay_plain(m):
    """Returns a list of problems. Empty list = PASS. A damaged archive gives problems, never a crash."""
    try:
        bad = replay_structure(m)
        if bad:
            return bad
        return replay_core(m)
    except Exception as exc:
        return ['the replay could not finish (%s: %s): the archive has a damaged part' % (exc.__class__.__name__, exc)]


def replay_core(m):
    """The whole replay, once the structure is known to be safe to walk."""
    problems = []
    recs = m['records']
    z = zero_state(m)
    if not recs:
        return ['no records']
    problems += replay_walks(m)
    problems += replay_turns(m)
    problems += replay_products(m)
    problems += replay_divisions(m)
    problems += replay_fractions(m)
    problems += replay_unknowns(m)
    problems += replay_planes(m)
    problems += replay_wanted(m)
    problems += replay_punknowns(m)
    problems += replay_proofs(m)
    problems += replay_corrections(m)
    problems += replay_deadlocks(m)
    problems += replay_tangents(m)
    problems += replay_approaches(m)
    problems += replay_differences(m)
    problems += replay_totals(m)
    problems += replay_recipes(m)
    problems += replay_identity(m)
    problems += replay_slots(m)
    problems += replay_stamps(m)
    problems += replay_meta(m)
    problems += replay_roles(m)
    expect = 0
    stamps = []
    for i, r in enumerate(recs):
        if r.get('id') != i:
            problems.append('record %d has the wrong id %r' % (i, r.get('id')))
        if i == 0:
            if r.get('value') != 0 or r.get('op') != 'Z0' or r.get('parents') != []:
                problems.append('record 0 is not Z0 (zero)')
        else:
            expect = S(expect)               # rebuild the count with S alone
            if r.get('op') != 'S' or r.get('parents') != [i - 1]:
                problems.append('record %d is not S of record %d' % (i, i - 1))
            if r.get('value') != expect:
                problems.append('record %d holds %r but S gives %r' % (i, r.get('value'), expect))
        if 'z0' not in r:
            problems.append('record %d never passed through Z0' % i)
        else:
            stamps.append(r['z0'])
        if len(problems) >= 20:
            problems.append('... more problems not listed')
            break
    if not problems:
        if len(set(stamps)) != len(stamps):
            problems.append('two records share one Z0 passage number')
        if z['record_passages'] != len(recs):
            problems.append('Z0 passage counter (%d) does not match the record count (%d)'
                            % (z['record_passages'], len(recs)))
        if z['operations'].get('S', 0) != len(recs) - 1:
            problems.append('Z0 saw %d S steps but there are %d'
                            % (z['operations'].get('S', 0), len(recs) - 1))
    return problems


def replay_walks(m):
    """Re-walk every pair with S links alone and check the role and stamps."""
    problems = []
    recs, exprs, roles = m['records'], m['expressions'], m['roles']
    z = zero_state(m)
    first = None
    for k, e in enumerate(exprs):
        if e.get('id') != k or not ref_ok(e.get('l'), len(recs)) or not ref_ok(e.get('r'), len(recs)):
            problems.append('expression %d has a wrong id or points outside the counter' % k)
            continue
        count = recs[e['r']]['value']
        if first is None and count >= 1:
            first = k
        n = e['l']
        for _ in range(count):              # S links only
            n = recs[n].get('nxt')
            if n is None:
                break
        if n is None or e['to'] != n or e['value'] != recs[n]['value']:
            problems.append('expression %d: walking S %d times from %d does not land on %r'
                            % (k, count, e['l'], e['to']))
        want = 'add' if (first is not None and k >= first) else 'walk'
        if e['op'] != want:
            problems.append('expression %d is called %r but should be %r' % (k, e['op'], want))
        if 'z0' not in e:
            problems.append('expression %d never passed through Z0' % k)
        if len(problems) >= 20:
            problems.append('... more problems not listed')
            return problems
    add = [r for r in roles if r['name'] == 'add']
    if first is None and add:
        problems.append('an addition role exists but no walk of one or more S steps has happened')
    if first is not None:
        if len(add) != 1 or add[0]['evidence'] != first \
                or add[0]['rule'] != ADD_ROLE_RULE or 'z0' not in add[0]:
            problems.append('the addition role is missing or does not match its first walk')
    for fam, key in (('expression', 'expressions'), ('role', 'roles')):
        st = [r['z0'] for r in m[key] if 'z0' in r]
        if len(set(st)) != len(st) or z[fam + '_passages'] != len(m[key]):
            problems.append('Z0 passage numbers for %s do not match' % key)
    if z['operations'].get('repeat_S', 0) != len(exprs):
        problems.append('Z0 saw %d walks but there are %d expressions'
                        % (z['operations'].get('repeat_S', 0), len(exprs)))
    for i, r in enumerate(recs):
        if i < len(recs) - 1 and r.get('nxt') != i + 1:
            problems.append('record %d has no S link to record %d' % (i, i + 1))
            break
        if i == len(recs) - 1 and r.get('nxt') is not None:
            problems.append('newest record already has an S link')
    return problems


def replay_turns(m):
    """Rebuild every S-or-turn path node from its parent and check the roles."""
    problems = []
    nodes, recs, roles = m['nodes'], m['records'], m['roles']
    z = zero_state(m)
    given = [r for r in roles if r['name'] == 'i']
    if len(given) != 1 or not given[0].get('given') or given[0]['rule'] != I_ACTION_RULE:
        problems.append('the given i action is missing or changed')
    ptr = m['turns']['ptr']
    if not nodes or nodes[0]['a'] != 'root' or nodes[0]['o'] != 0:
        return problems + ['the first path node is not the root at 0']
    idx, roots = 1, 1
    for e in range(ptr):                       # every expansion made an S child and a turn child
        if idx + 1 > len(nodes) - 1:
            problems.append('expansion %d is missing its children' % e)
            return problems
        a, b = nodes[idx], nodes[idx + 1]
        if (a['a'], a['p'], b['a'], b['p']) != ('S', e, 'I', e):
            problems.append('nodes %d and %d are not the S and turn children of node %d' % (idx, idx + 1, e))
            return problems
        idx += 2
        if idx < len(nodes) and nodes[idx]['a'] == 'root':
            if nodes[idx]['o'] != roots:
                problems.append('root node %d starts at %r, expected counter record %d'
                                % (idx, nodes[idx]['o'], roots))
                return problems
            roots += 1
            idx += 1
    if idx != len(nodes) or roots != m['turns']['roots']:
        problems.append('the node list does not match the expansions that were made')
        return problems
    s_nodes = i_nodes = 0
    for pos, n in enumerate(nodes):
        k = n['id']
        if k != pos:
            problems.append('node at position %d carries id %r' % (pos, k))
        if n['a'] == 'root':
            want_c, want_d, want_cx, want_tr = [recs[n['o']]['value'], 0, 0, 0], 0, False, 0
        else:
            par = nodes[n['p']]
            if n['o'] != par['o']:
                problems.append('node %d starts somewhere else than its parent' % k)
                continue
            if n['a'] == 'S':
                want_c, want_cx = unit_step(par['c'], par['d'])
                want_d = par['d']
                want_tr = 0
                s_nodes += 1
            else:
                want_c, want_d, want_cx, want_tr = list(par['c']), turn(par['d']), False, par['tr'] + 1
                i_nodes += 1
        if n['c'] != want_c or n['d'] != want_d or n['cx'] != want_cx or n['tr'] != want_tr:
            problems.append('node %d: its parent and action do not give its state' % k)
        if 'z0' not in n:
            problems.append('node %d never passed through Z0' % k)
        if len(problems) >= 20:
            problems.append('... more problems not listed')
            return problems
    for name, test, why in TURN_ROLES:
        first = next((n['id'] for n in nodes if test(n)), None)
        found = [r for r in roles if r['name'] == name]
        if first is None and found:
            problems.append('role %s exists but no path shows it' % name)
        elif first is not None and (len(found) != 1 or found[0].get('evidence') != first or 'z0' not in found[0]):
            problems.append('role %s is missing or does not match the first path that shows it' % name)
    st = [n['z0'] for n in nodes if 'z0' in n]
    if len(set(st)) != len(st) or z['node_passages'] != len(nodes):
        problems.append('Z0 passage numbers for path nodes do not match')
    if z['operations'].get('Sd', 0) != s_nodes or z['operations'].get('I', 0) != i_nodes:
        problems.append('Z0 saw %d S steps and %d turns on paths but the nodes show %d and %d'
                        % (z['operations'].get('Sd', 0), z['operations'].get('I', 0), s_nodes, i_nodes))
    return problems


def replay_products(m):
    """Redo every repeated add and repeated turn, with S steps and turns only."""
    problems = []
    prods, recs, roles = m['products'], m['records'], m['roles']
    z = zero_state(m)
    # walk the pair order explicitly
    order = []
    nn = 0
    auto = 0                                # position among the records the engine made itself
    while len(order) < (len(prods) + 1) // 2 + 1:
        for ii in range(nn + 1):
            order.append((nn, ii))
            if ii != nn:
                order.append((ii, nn))
        nn += 1
    for k, p in enumerate(prods):
        if p.get('manual'):
            a, b = p['l'], p['r']
            if p.get('id') != k:
                problems.append('product record %d has the wrong id' % k)
                break
        else:
            a, b = order[auto // 2]
            if p.get('id') != k or p['kind'] != ('multiply' if auto % 2 == 0 else 'rotate') \
                    or (p['l'], p['r']) != (a, b):
                problems.append('product record %d is out of the pair order' % k)
                break
            auto += 1
        if a >= len(recs) or b >= len(recs):
            problems.append('product record %d points outside the counter' % k)
            continue
        base, count = recs[a]['value'], recs[b]['value']
        skipped = k in REPLAY_SKIP['products']      # unchanged since it was redone from S earlier in this launch
        if p['kind'] == 'multiply':
            if p['status'] == 'done':
                if not skipped:
                    r = repeat_add(base, count, len(recs))
                    if r is None or p['v'] != [r, 0]:
                        problems.append('product record %d: adding %d, %d times does not give %s' % (k, base, count, p['v']))
            elif p['status'] == 'parked':
                if p['v'] is not None or k not in m['mul_parked']:
                    problems.append('product record %d is parked but has a value or is not on the parked list' % k)
                elif not skipped and repeat_add(base, count, p['limit']) is not None:
                    problems.append('product record %d was parked but fits in the counter' % k)
            else:
                problems.append('product record %d has an unknown status' % k)
            if p['op'] not in ('multiply', 'repeat_add') or (p['op'] == 'multiply' and not find_role(m, 'multiply')):
                problems.append('product record %d is named %r before multiply was found' % (k, p['op']))
        else:
            if not skipped and p['v'] != repeat_turn(base, count):
                problems.append('product record %d: turning %d, %d times does not give %s' % (k, base, count, p['v']))
            if p['op'] not in ('rotate', 'repeat_turn') or (p['op'] == 'rotate' and not find_role(m, 'rotate')):
                problems.append('product record %d is named %r before rotate was found' % (k, p['op']))
        if 'z0' not in p:
            problems.append('product record %d never passed through Z0' % k)
        if len(problems) >= 20:
            problems.append('... more problems not listed')
            return problems
    if sorted(m['mul_parked']) != [p['id'] for p in prods if p['status'] == 'parked']:
        problems.append('the parked list for products does not match')
    # the roles: each must point at a record that really shows it, and exist iff one does
    has_mul = any(p['kind'] == 'multiply' and p['status'] == 'done' and recs[p['r']]['value'] >= 2 for p in prods)
    has_rot = any(p['kind'] == 'rotate' and p['v'] != [recs[p['l']]['value'], 0] for p in prods)
    for name, exists, kind in (('multiply', has_mul, 'multiply'), ('rotate', has_rot, 'rotate')):
        found = [r for r in roles if r['name'] == name]
        if exists and (len(found) != 1 or 'z0' not in found[0] or found[0]['rule'] != MUL_ROLE_RULE
                       or prods[found[0]['evidence']]['kind'] != kind):
            problems.append('role %s is missing or points at the wrong record' % name)
        if not exists and found:
            problems.append('role %s exists but no product shows it' % name)
    st_ = [p['z0'] for p in prods if 'z0' in p]
    if len(set(st_)) != len(st_) or z['product_passages'] != len(prods):
        problems.append('Z0 passage numbers for products do not match')
    if z['operations'].get('repeat_add', 0) < sum(1 for p in prods if p['kind'] == 'multiply') \
            or z['operations'].get('repeat_turn', 0) != sum(1 for p in prods if p['kind'] == 'rotate'):
        problems.append('Z0 saw fewer repeated adds or turns than there are product records')
    return problems


def replay_divisions(m):
    """Split and regroup every pair again, from the units."""
    problems = []
    divs, recs, roles = m['divisions'], m['records'], m['roles']
    z = zero_state(m)
    order, nn, auto = [], 0, 0
    while len(order) < len(divs) + 2:
        for ii in range(nn + 1):
            order.append((nn, ii))
            if ii != nn:
                order.append((ii, nn))
        nn += 1
    has = {'divide': False, 'remainder': False}
    for k, d in enumerate(divs):
        if d.get('manual'):
            a, b = d['l'], d['r']
            if d.get('id') != k:
                problems.append('division record %d has the wrong id' % k)
                break
        else:
            a, b = order[auto]
            if d.get('id') != k or (d['l'], d['r']) != (a, b):
                problems.append('division record %d is out of the pair order' % k)
                break
            auto += 1
        if a >= len(recs) or b >= len(recs):
            problems.append('division record %d points outside the counter' % k)
            continue
        out = regroup(recs[a]['value'], recs[b]['value'])
        if out is None:
            if d['status'] != 'blocked' or d['q'] is not None or d.get('rem') is not None \
                    or d.get('zeros') is not None or d.get('reason') != 'division_by_zero' or d.get('op') != 'regroup':
                problems.append('division record %d divides by nothing but is not blocked' % k)
        else:
            q, rem, zeros = out
            if d['status'] != 'done' or (d['q'], d['rem'], d['zeros']) != (q, rem, zeros):
                problems.append('division record %d: splitting %d into groups of %d should give %d, %d left, %d zeros'
                                % (k, recs[a]['value'], recs[b]['value'], q, rem, zeros))
            has['divide'] = has['divide'] or zeros >= 1
            has['remainder'] = has['remainder'] or rem >= 1
            if d['op'] not in ('divide', 'regroup') or (d['op'] == 'divide' and not find_role(m, 'divide')):
                problems.append('division record %d is named %r before divide was found' % (k, d['op']))
        if 'z0' not in d:
            problems.append('division record %d never passed through Z0' % k)
        if len(problems) >= 20:
            problems.append('... more problems not listed')
            return problems
    for name in ('divide', 'remainder'):
        found = [r for r in roles if r['name'] == name]
        if has[name] and (len(found) != 1 or 'z0' not in found[0] or found[0]['rule'] != DIV_ROLE_RULE
                          or divs[found[0]['evidence']]['status'] != 'done'):
            problems.append('role %s is missing or points at the wrong record' % name)
        if not has[name] and found:
            problems.append('role %s exists but no division shows it' % name)
    st_ = [d['z0'] for d in divs if 'z0' in d]
    if len(set(st_)) != len(st_) or z['division_passages'] != len(divs):
        problems.append('Z0 passage numbers for divisions do not match')
    if z['operations'].get('regroup', 0) != len(divs):
        problems.append('Z0 saw %d splits but there are %d division records' % (z['operations'].get('regroup', 0), len(divs)))
    return problems


def replay_fractions(m):
    """Find every leftover again and follow the records again."""
    problems = []
    fr, divs, recs, roles = m['fractions'], m['divisions'], m['records'], m['roles']
    z = zero_state(m)
    if m['fcursor'] > len(divs):
        return ['the fraction cursor is past the end of the divisions']
    want = [i for i in range(m['fcursor']) if divs[i]['status'] == 'done' and divs[i]['rem'] >= 1]
    if [f['div'] for f in fr] != want:
        return ['the fractions are not exactly the leftovers of the divisions looked at so far']
    has = {'fraction': bool(fr), 'reduce': False}
    for k, f in enumerate(fr):
        d = divs[f['div']]
        b = recs[d['r']]['value']
        got = fraction_chain(m, d['rem'], b)
        if got is None:
            problems.append('fraction record %d: the divisions it followed are missing' % k)
            continue
        g, rr, bb, chain = got
        if f.get('id') != k or (f['q'], f['r'], f['b']) != (d['q'], d['rem'], b) \
                or (f['g'], f['rr'], f['bb'], f['steps'], f['chain']) != (g, rr, bb, len(chain) - 2, chain) \
                or f['key'] != [d['q'], rr, bb]:
            problems.append('fraction record %d: %d left of %d should be written %d of %d (split by %d)'
                            % (k, d['rem'], b, rr, bb, g))
        has['reduce'] = has['reduce'] or g >= 2
        if 'z0' not in f:
            problems.append('fraction record %d never passed through Z0' % k)
        if len(problems) >= 20:
            problems.append('... more problems not listed')
            return problems
    for name in ('fraction', 'reduce'):
        found = [r for r in roles if r['name'] == name]
        if has[name] and (len(found) != 1 or 'z0' not in found[0] or found[0]['rule'] != FRAC_ROLE_RULE):
            problems.append('role %s is missing or changed' % name)
        if not has[name] and found:
            problems.append('role %s exists but no leftover shows it' % name)
    st_ = [f['z0'] for f in fr if 'z0' in f]
    if len(set(st_)) != len(st_) or z['fraction_passages'] != len(fr):
        problems.append('Z0 passage numbers for fractions do not match')
    return problems


def replay_unknowns(m):
    """Try every blank again from the counter, shape by shape, and go backwards again."""
    problems = []
    us, recs, roles = m['unknowns'], m['records'], m['roles']
    z = zero_state(m)
    order, nn, auto = [], 0, 0
    while len(order) < len(us) + 2:
        for ii in range(nn + 1):
            order.append((nn, ii))
            if ii != nn:
                order.append((ii, nn))
        nn += 1
    if us and slots_waiting(m):
        problems.append('blanks were tried before ' + ' and '.join(slots_waiting(m)) + ' were found')
    first = {}
    for k, u in enumerate(us):
        if u.get('manual'):
            a, b = u['l'], u['r']
            if u.get('id') != k:
                problems.append('blank record %d has the wrong id' % k)
                break
        else:
            a, b = order[auto]
            if u.get('id') != k or (u['l'], u['r']) != (a, b):
                problems.append('blank record %d is out of the pair order' % k)
                break
            auto += 1
        if a >= len(recs) or b >= len(recs) or u['limit'] > len(recs):
            problems.append('blank record %d points outside the counter' % k)
            continue
        av, cv = recs[a]['value'], recs[b]['value']
        if k in REPLAY_SKIP['unknowns']:     # unchanged since it was re-solved from S earlier in this launch
            ncand, forms = u['tried'], u['forms']
        else:
            ncand, forms = solve_pair(av, cv, u['limit'], lambda op, A, B: rational(op, A, B, u['limit']),
                                      lambda q: signed_walk(0, q, 2), lambda op, side: undo(op, side, av, cv))
        if u['tried'] != ncand or u['forms'] != forms:
            bad = [i for i, (x, y) in enumerate(zip(u['forms'], forms)) if x != y] or ['count']
            problems.append('blank record %d (%d and %d): shape %s tried again gives something different'
                            % (k, av, cv, bad[0]))
        else:
            for fi, f in enumerate(forms):
                for name in unknown_all_names(f, ncand):
                    first.setdefault(name, (k, fi))
        if 'z0' not in u:
            problems.append('blank record %d never passed through Z0' % k)
        if len(problems) >= 20:
            problems.append('... more problems not listed')
            return problems
    names = set(UNKNOWN_WHY)
    for name in names:
        found = [r for r in roles if r['name'] == name]
        if name in first:
            if len(found) != 1 or 'z0' not in found[0] or found[0]['rule'] != X_ROLE_RULE \
                    or (found[0]['evidence'], found[0]['form']) != first[name]:
                problems.append('role %s is missing or changed' % name)
        elif found:
            problems.append('role %s exists but no blank shows it' % name)
    st_ = [u['z0'] for u in us if 'z0' in u]
    if len(set(st_)) != len(st_) or z['unknown_passages'] != len(us):
        problems.append('Z0 passage numbers for blanks do not match')
    if z['operations'].get('undo', 0) != 8 * len(us):
        problems.append('Z0 saw %d backward steps but there are %d blank shapes'
                        % (z['operations'].get('undo', 0), 8 * len(us)))
    return problems


def replay_planes(m):
    """Find every point again from the paths, and redraw every look."""
    problems = []
    pl, nodes, views, roles = m['planes'], m['nodes'], m['views'], m['roles']
    z = zero_state(m)
    if m['plane_cur'] > len(nodes):
        return ['the plane cursor is past the end of the path nodes']
    seen, want = {}, []
    for nid in range(m['plane_cur']):
        v = node_value(nodes[nid]['c'])
        if v not in seen:
            seen[v] = len(want)
            want.append((v, nid))
    if len(want) != len(pl):
        return ['the plane holds %d points but the paths reach %d' % (len(pl), len(want))]
    first = {}
    for k, ((v, nid), p) in enumerate(zip(want, pl)):
        if p.get('id') != k or tuple(p['p']) != v or p['node'] != nid or p['place'] != plane_place(v):
            problems.append('plane point %d does not match the path node it came from' % k)
        for name in plane_role_names(v):
            first.setdefault(name, k)
        if 'z0' not in p:
            problems.append('plane point %d never passed through Z0' % k)
        if len(problems) >= 20:
            problems.append('... more problems not listed')
            return problems
    for name in PLANE_WHY:
        found = [r for r in roles if r['name'] == name]
        if name in first:
            if len(found) != 1 or 'z0' not in found[0] or found[0]['rule'] != PLANE_RULE or found[0]['evidence'] != first[name]:
                problems.append('role %s is missing or changed' % name)
        elif found:
            problems.append('role %s exists but no point shows it' % name)
    for k, v in enumerate(views):
        if v.get('id') != k or v['n'] > len(pl) or not 1 <= v['r'] <= 15:
            problems.append('look %d is out of order or looks past the plane' % k)
            continue
        if v['rows'] != look(v['r'], [tuple(p['p']) for p in pl[:v['n']]], v.get('fmt', 1)):
            problems.append('look %d draws something different when redrawn' % k)
        if 'z0' not in v:
            problems.append('look %d never passed through Z0' % k)
    st_ = [p['z0'] for p in pl if 'z0' in p]
    if len(set(st_)) != len(st_) or z['plane_passages'] != len(pl):
        problems.append('Z0 passage numbers for plane points do not match')
    st_ = [v['z0'] for v in views if 'z0' in v]
    if len(set(st_)) != len(st_) or z['view_passages'] != len(views):
        problems.append('Z0 passage numbers for looks do not match')
    if z['operations'].get('look', 0) != len(views):
        problems.append('Z0 saw %d looks but there are %d look records' % (z['operations'].get('look', 0), len(views)))
    return problems


def replay_wanted(m):
    """Every want is checked again against what the engine has built."""
    problems = []
    ws = m['wanted']
    z = zero_state(m)
    keys = set()
    for k, w in enumerate(ws):
        key = tuple(w['key'])
        if w.get('id') != k or key in keys or w.get('text') != want_text(key) or w.get('asks', 0) < 1:
            problems.append('want %d is out of order, repeated, or changed' % k)
        keys.add(key)
        if w['status'] == 'found':
            ptr = w.get('by')
            if not ptr or not want_match(m, key, ptr) or not isinstance(w.get('found_run'), int):
                problems.append('want %d (%s) says it was found but the record it points at does not answer it' % (k, w['text']))
        elif w['status'] == 'open':
            if want_answer(m, key) is not None:
                problems.append('want %d (%s) is still open but the engine can answer it now' % (k, w['text']))
        else:
            problems.append('want %d has an unknown status' % k)
        if 'z0' not in w:
            problems.append('want %d never passed through Z0' % k)
        if len(problems) >= 20:
            problems.append('... more problems not listed')
            return problems
    st_ = [w['z0'] for w in ws if 'z0' in w]
    if len(set(st_)) != len(st_) or z['want_passages'] != len(ws):
        problems.append('Z0 passage numbers for wants do not match')
    return problems


def replay_punknowns(m):
    """Try every blank on the plane again, shape by shape, and go backwards again."""
    problems = []
    us, pl, roles = m['punknowns'], m['planes'], m['roles']
    z = zero_state(m)
    order, nn, auto = [], 0, 0
    while len(order) < len(us) + 2:
        for ii in range(nn + 1):
            order.append((nn, ii))
            if ii != nn:
                order.append((ii, nn))
        nn += 1
    if us and slots_waiting(m):
        problems.append('plane blanks were tried before ' + ' and '.join(slots_waiting(m)) + ' were found')
    first = {}
    for k, u in enumerate(us):
        if u.get('manual'):
            l, r = u['l'], u['r']
            if u.get('id') != k:
                problems.append('plane blank record %d has the wrong id' % k)
                break
        else:
            l, r = order[auto]
            if u.get('id') != k or (u['l'], u['r']) != (l, r):
                problems.append('plane blank record %d is out of the pair order' % k)
                break
            auto += 1
        if l >= len(pl) or r >= len(pl) or u['n'] > len(pl) or u['limit'] > len(m['records']) or max(l, r) >= u['n']:
            problems.append('plane blank record %d points outside the plane' % k)
            continue
        a, c = tuple(pl[l]['p']), tuple(pl[r]['p'])
        if k in REPLAY_SKIP['punknowns']:    # unchanged since it was re-solved from S earlier in this launch
            ncands, forms = u['tried'], u['forms']
        else:
            cands = px_candidates(m, a, c, u['n'], u.get('xp', XP_BOUND))
            forms = psolve(cands, a, c, lambda op, A, B: cplx(op, A, B, u['limit']), lambda op, side: undo2(op, side, a, c))
            ncands = len(cands)
        if u['tried'] != ncands or u['forms'] != forms:
            bad = [i for i, (x, y) in enumerate(zip(u['forms'], forms)) if x != y] or ['count']
            problems.append('plane blank record %d (%s and %s): shape %s tried again gives something different'
                            % (k, value_text(a), value_text(c), bad[0]))
        else:
            for fi, f in enumerate(forms):
                for name in punknown_names(f, a, ncands):
                    first.setdefault(name, (k, fi))
        if 'z0' not in u:
            problems.append('plane blank record %d never passed through Z0' % k)
        if len(problems) >= 20:
            problems.append('... more problems not listed')
            return problems
    for name in PUNKNOWN_WHY:
        found = [r for r in roles if r['name'] == name]
        if name in first:
            if len(found) != 1 or 'z0' not in found[0] or found[0]['rule'] != XP_ROLE_RULE \
                    or (found[0]['evidence'], found[0]['form']) != first[name]:
                problems.append('role %s is missing or changed' % name)
        elif found:
            problems.append('role %s exists but no plane blank shows it' % name)
    st_ = [u['z0'] for u in us if 'z0' in u]
    if len(set(st_)) != len(st_) or z['punknown_passages'] != len(us):
        problems.append('Z0 passage numbers for plane blanks do not match')
    if z['operations'].get('undo2', 0) != 8 * len(us):
        problems.append('Z0 saw %d backward steps on the plane but there are %d shapes'
                        % (z['operations'].get('undo2', 0), 8 * len(us)))
    return problems


def replay_proofs(m):
    """Hide every number again and search again."""
    problems = []
    ps, log, roles = m['proofs'], m['slot_log'], m['roles']
    z = zero_state(m)
    if ps and slots_waiting(m):
        problems.append('proofs were made before ' + ' and '.join(slots_waiting(m)) + ' were found')
    cur, first = [0, 0], {}
    for k, p in enumerate(ps):
        if p.get('id') != k or p['slot'] >= len(log):
            problems.append('proof %d is out of order or points outside the slot fillings' % k)
            break
        slot = log[p['slot']]
        if not p.get('manual'):
            if [p['slot'], p['g'] if p['g'] is not None else 0] != cur:
                problems.append('proof %d is out of the walking order' % k)
                break
        if p['status'] == 'blocked':
            if slot['status'] != 'blocked' or p['g'] is not None or p['why'] != slot['why']:
                problems.append('proof %d says the filling is blocked but it is not' % k)
            nxt = [p['slot'] + 1, 0]
        else:
            if slot['status'] != 'done':
                problems.append('proof %d: slot filling %d is not done' % (k, p['slot']))
                break
            groups, ops, nums = proof_parts(m, slot)
            if not 0 <= p['g'] < len(groups) or p['n'] > len(m['planes']) or p['limit'] > len(m['records']):
                problems.append('proof %d points outside the filling or the plane' % k)
                break
            orig = nums[p['g']]
            cands, top = proof_candidates(m, orig, p['n'], p.get('pb', PROOF_BOUND), p.get('xb', XP_BOUND))
            xs, over, blocks = proof_search((ops, nums), p['g'], (slot['value'], slot['im'], slot['den']), cands,
                                            lambda op, a, b: slotop(op, a, b, p['limit']))
            if (p['xs'], p['over'], p['blocks'], p['tried'], p['bound'], p['orig']) != (xs, over, blocks, len(cands), top, list(orig)) \
                    or p['found_orig'] != (list(orig) in xs) or p['text'] != proof_text(m, slot, p['g']):
                problems.append('proof %d (%s): hiding the number and searching again gives something different' % (k, p['text']))
            for name in proof_names(p):
                first.setdefault(name, k)
            nxt = [p['slot'] + 1, 0] if p['g'] + 1 >= len(groups) else [p['slot'], p['g'] + 1]
        if not p.get('manual'):
            cur = nxt
        if 'z0' not in p:
            problems.append('proof %d never passed through Z0' % k)
        if len(problems) >= 20:
            problems.append('... more problems not listed')
            return problems
    if not problems and m['proof_cur'] != cur:
        problems.append('the proof cursor %s should be %s' % (m['proof_cur'], cur))
    for name in PROOF_WHY:
        found = [r for r in roles if r['name'] == name]
        if name in first:
            if len(found) != 1 or 'z0' not in found[0] or found[0]['rule'] != PROOF_RULE or found[0]['evidence'] != first[name]:
                problems.append('role %s is missing or changed' % name)
        elif found:
            problems.append('role %s exists but no proof shows it' % name)
    st_ = [p['z0'] for p in ps if 'z0' in p]
    if len(set(st_)) != len(st_) or z['proof_passages'] != len(ps):
        problems.append('Z0 passage numbers for proofs do not match')
    return problems


def replay_slots(m):
    """Redo every slot filling from its template and number, with S steps, turns and splits only."""
    problems = []
    log, recs, roles = m['slot_log'], m['records'], m['roles']
    z = zero_state(m)
    given = [r for r in roles if r['name'] == SLOT_TEMPLATE]
    if len(given) != 1 or not given[0].get('given') or given[0]['rule'] != SLOT_RULE:
        problems.append('the given 00404 template is missing or changed')
    if log and slots_waiting(m):
        problems.append('slots were used before ' + ' and '.join(slots_waiting(m)) + ' were found')
    refset = set(m['slot_refs']) | set(m['slot_prefs'])
    if len(refset) != len(m['slot_refs']) + len(m['slot_prefs']) or m['slot_refs'][0] != SLOT_TEMPLATE:
        problems.append('the slot template list repeats a template or lost 00404')
    seen = {}
    used = 0
    for k, r in enumerate(log):
        key = r['ref'] + '|' + SLOT_SIG
        symbols = breakdown(r['ref'])
        if r['ref'] not in refset:
            problems.append('slot filling %d uses a template that is not on the template list' % k)
            break
        if r.get('id') != k or r['n'] != seen.get(key, 0):
            problems.append('slot filling %d is out of order for template %s' % (k, r['ref']))
            break
        seen[key] = r['n'] + 1
        if r['n'] >= len(SLOT_OPS) ** (len(symbols) - 1):
            problems.append('slot filling %d is beyond the end of template %s' % (k, r['ref']))
            break
        choice = slot_filling(symbols, r['n'])
        nums, ops = slot_numbers(symbols, choice, r['limit'])
        need = slot_need(nums, r['limit'])
        if r['need'] != need or r['text'] != slot_text(symbols, choice) or r['used'] != len(ops):
            problems.append('slot filling %d (%s) does not match its template and filling number' % (k, r['text']))
        elif r['status'] == 'parked':
            if r['value'] is not None or k not in m['slot_parked']:
                problems.append('slot filling %d is parked but has a value or is not on the parked list' % k)
            elif r['need'] < r['limit'] and evaluate_slot(nums, ops, lambda o, a, b: slotop(o, a, b, r['limit'])) is not None:
                problems.append('slot filling %d (%s) was parked but fits in the counter' % (k, r['text']))
        elif r['status'] == 'blocked':
            if r['value'] is not None or r['need'] >= r['limit'] or r.get('why') not in BLOCKS or \
                    evaluate_slot(nums, ops, lambda o, a, b: slotop(o, a, b, r['limit'])) != r['why']:
                problems.append('slot filling %d (%s) is blocked but redoing it does not block' % (k, r['text']))
            used += 1
        elif r['status'] == 'done':
            if r['need'] >= len(recs):
                problems.append('slot filling %d uses a number the counter never reached' % k)
            else:
                acc = evaluate_slot(nums, ops, lambda o, a, b: slotop(o, a, b, len(recs)))
                used += len(ops)
                if not isinstance(acc, tuple) or (r['value'], r['im'], r['den']) != acc:
                    problems.append('slot filling %d (%s): it should give %s' % (k, r['text'], acc))
        else:
            problems.append('slot filling %d has an unknown status' % k)
        if 'z0' not in r:
            problems.append('slot filling %d never passed through Z0' % k)
        if len(problems) >= 20:
            problems.append('... more problems not listed')
            break                      # the later checks below still run
    for key, st in m['slots'].items():
        if st['next'] != seen.get(key, 0):
            problems.append('template %s says %d fillings were tried but %d are saved'
                            % (st['ref'], st['next'], seen.get(key, 0)))
    if sorted(m['slot_parked']) != [r['id'] for r in log if r['status'] == 'parked']:
        problems.append('the parked list does not match the parked fillings')
    st_ = [r['z0'] for r in log if 'z0' in r]
    if len(set(st_)) != len(st_) or z['slot_passages'] != len(log):
        problems.append('Z0 passage numbers for slot fillings do not match')
    if z['operations'].get('slotop', 0) < used:
        problems.append('Z0 saw only %d slot operations but the fillings used %d'
                        % (z['operations'].get('slotop', 0), used))
    return problems


def replay_report(m, problems=None):
    if problems is None:
        problems = replay(m)
        if not problems:
            verified(m)
            take_snapshot(m)
    if problems:
        print('  Independent replay: FAIL')
        for p in problems:
            print('    -', p)
    else:
        print('  Independent replay: PASS (%d records rebuilt from 0 with S alone; '
              '%d walked pairs re-walked; %d products and turns redone; %d divisions split again; %d fractions found again; %d blanks tried again; %d plane points and %d looks redone; %d wants rechecked; %d plane blanks tried again; %d proofs redone; %d corrections kept; %d deadlocks rechecked; %d tangents rechecked; %d approaches rechecked; %d differences rechecked; %d totals rechecked; %d path nodes rebuilt; '
              '%d slot fillings redone)'
              % (len(m['records']), len(m['expressions']), len(m['products']), len(m['divisions']),
                 len(m['fractions']), len(m['unknowns']), len(m['planes']), len(m['views']), len(m['wanted']), len(m['punknowns']), len(m['proofs']), len(m['corrections']), len(m['deadlocks']), len(m['tangents']), len(m['approaches']), len(m['differences']), len(m['totals']), len(m['nodes']), len(m['slot_log'])))
    return not problems


# ---------------- showing results ----------------

def print_stats(m):
    flush_inner(m) if GATE['m'] is m else 0
    z = zero_state(m)
    print('  Total records:', len(m['records']),
          '| newest value:', m['records'][-1]['value'])
    print('  Every record has a global id: %d handed out, each with its recipe and clocks' % z['gids'])
    print('  Through Z0: %d passages | stamped: %d counter, %d walks, %d products, %d divisions, %d fractions, %d blanks, %d plane points, %d looks, %d wants, %d plane blanks, %d proofs, %d corrections, %d deadlocks, %d tangents, %d approaches, %d differences, %d totals, %d path nodes, %d slot fillings, %d roles | late %d'
          % (z['passages'], z['record_passages'], z['expression_passages'], z['product_passages'],
             z['division_passages'], z['fraction_passages'], z['unknown_passages'], z['plane_passages'], z['view_passages'], z['want_passages'], z['punknown_passages'], z['proof_passages'], z['correction_passages'], z['deadlock_passages'], z['tangent_passages'], z['approach_passages'], z['difference_passages'], z['total_passages'], z['node_passages'], z['slot_passages'],
             z['role_passages'], z['late_passages']))
    kinds = {}
    for v in NODE_INDEX:
        k = 'real >= 0' if v[1] == 0 and v[0] >= 0 else 'negative real' if v[1] == 0 else 'has i'
        kinds[k] = kinds.get(k, 0) + 1
    print('  Fractions: %d leftover parts | distinct values: %d | written in fewer parts: %d | roles found: %s'
          % (len(m['fractions']), len(set(tuple(f['key']) for f in m['fractions'])),
             sum(1 for f in m['fractions'] if f['g'] >= 2),
             ', '.join(r['name'] for r in m['roles'] if r.get('kind') == 'fraction') or 'none yet'))
    print(plane_status(m))
    print(wanted_status(m))
    print(correction_status(m))
    print(proof_status(m))
    print(punknown_status(m))
    print(unknown_status(m))
    print(deadlock_status(m))
    print(tangent_status(m))
    print(approach_status(m))
    print(difference_status(m))
    print(total_status(m))
    print('  Divisions: %d records (%d blocked) | roles found: %s'
          % (len(m['divisions']), sum(1 for d in m['divisions'] if d['status'] == 'blocked'),
             ', '.join(r['name'] for r in m['roles'] if r.get('kind') == 'division') or 'none yet'))
    print('  Products: %d records (%d parked) | roles found: %s'
          % (len(m['products']), len(m['mul_parked']),
             ', '.join(r['name'] for r in m['roles'] if r.get('kind') == 'product') or 'none yet'))
    print('  00404 slots: %d fillings tried, %d parked | waiting for: %s'
          % (len(m['slot_log']), len(m['slot_parked']), ' '.join(slots_waiting(m)) or 'nothing'))
    print('  Paths: %d nodes, %d expanded | distinct values on paths: %d %s'
          % (len(m['nodes']), m['turns']['ptr'], len(NODE_INDEX), kinds))
    print('  Walked pairs: %d | roles found: %s | pair work at (%d, %d) of %d counted'
          % (len(m['expressions']), ', '.join(r['name'] for r in m['roles']) or 'none yet',
             m['pairs']['n'], m['pairs']['i'], len(m['records'])))
    print('  Operations seen by Z0:', z['operations'] or 'none yet')


def full_line(m, idx):
    r = m['records'][idx]
    if r['op'] == 'Z0':
        return '#%d  0  [Z0, the zero gate itself]' % idx
    return '#%d  S(#%d) = %s' % (idx, r['parents'][0], r['value'])


def expr_text(e):
    return '%d + %d = %d' % (e['l'], e['r'], e['value']) if e['op'] == 'add' \
        else '%d walked %d S steps = %d' % (e['l'], e['r'], e['value'])


def ways(m, n, limit=10):
    found = [e for e in m['expressions'] if e['value'] == n]
    print('  Found by walking pairs: %d way(s)' % len(found))
    for e in found[:limit]:
        print('    #%d  %s   recipe: %s'
              % (e['id'], expr_text(e), recipe_add(e['l'], m['records'][e['r']]['value'])))
    if len(found) > limit:
        print('    ... and %d more' % (len(found) - limit))


def parse_value(text):
    s = text.replace(' ', '').lower()
    if not s:
        return None
    if 'i' not in s:
        return (int(s), 0) if re.fullmatch(r'[+-]?\d+', s) else None
    g = re.fullmatch(r'([+-]?\d+)?([+-]?)(\d*)i', s)
    if not g:
        return None
    r, sign, digits = g.groups()
    if r is not None and sign == '' and digits == '':
        return (0, int(r))                  # such as 3i or -3i
    im = int(digits) if digits else 1
    return (int(r) if r else 0, -im if sign == '-' else im)


def node_ways(m, v, limit=8):
    ids = NODE_INDEX.get(v, [])
    print('  Found on S-and-turn paths: %d way(s)' % len(ids))
    for nid in ids[:limit]:
        origin, word = node_word(m, nid)
        print('    node #%d  start at %d, then: %s   recipe: %s' % (nid, origin, word, recipe_node(m, nid)))
    if len(ids) > limit:
        print('    ... and %d more' % (len(ids) - limit))
    if not ids:
        print('  Not made yet. That does not mean it can never be made.')


def lookup_fraction(m, text):
    g = re.fullmatch(r'([+-]?\d+)/(\d+)', text.replace(' ', ''))
    if not g:
        return False
    p, q = int(g.group(1)), int(g.group(2))
    if q == 0:
        print('\nValue %d/0: a group of no units can never fill, so it is blocked.' % p)
        return True
    facing = 2 if p < 0 else 0
    p = abs(p)
    if max(p, q) >= len(m['records']):
        print('\nValue %s%d/%d: the counter has only reached %d, so this is not worked out now.'
              % ('-' if facing else '', p, q, len(m['records']) - 1))
        want_check(m, ('count', max(p, q)), False)
        return True
    whole, rem, _z = regroup(p, q)
    if rem == 0:
        return lookup(m, str(whole if not facing else -whole))
    got = fraction_chain(m, rem, q)
    sign = '-' if facing else ''
    if got is None:
        print('\nValue %s%d/%d = %s' % (sign, p, q, mixed(sign, whole, rem, q)))
        print('  Its fewest parts are not known yet: the splits it needs are not in the divisions archive.')
        want_check(m, ('fracq', whole, rem, q), False)
        want_check(m, ('count', max(rem, q)), max(rem, q) < len(m['records']))
        return True
    gg, rr, bb, _chain = got
    print('\nValue %s%d/%d = %s (fewest parts: %d of %d)' % (sign, p, q, mixed(sign, whole, rem, q), rr, bb))
    fraction_ways(m, whole, rr, bb, facing)
    want_check(m, ('fraction', whole, rr, bb), bool([f for f in m['fractions'] if f['key'] == [whole, rr, bb]]))
    num = rr + whole * bb
    hits = [r for r in m['slot_log'] if r['status'] == 'done' and r['den'] == bb and not r['im'] and r['value'] == (-num if facing else num)]
    print('  Found in 00404 slot fillings: %d way(s)' % len(hits))
    for r in hits[:5]:
        print('    ' + slot_line(m, r))
    if len(hits) > 5:
        print('    ... and %d more' % (len(hits) - 5))
    want_check(m, ('slot', -num if facing else num, bb), bool(hits))
    return True


def lookup(m, text):
    g_ = re.fullmatch(r'x=(.+)|(.+)=x', text.replace(' ', '').lower())
    if g_:
        v_ = g_.group(1) or g_.group(2)
        if parse_value(v_) is not None or re.fullmatch(r'[+-]?\d+/\d+', v_):
            print('\nx = %s is already the answer. Looking up %s:' % (v_, v_))
            return lookup(m, v_)
    if 'x' in text.lower():
        return lookup_punknown(m, text) or lookup_unknown(m, text)
    if '/' in text:
        return lookup_fraction(m, text)
    v = parse_value(text)
    if v is None:
        return False
    print('\nValue %s:' % value_text(v))
    if v[1] == 0 and v[0] >= 0:
        want_check(m, ('count', v[0]), v[0] < len(m['records']))
    if v[1] == 0 and 0 <= v[0] < len(m['records']):
        n = v[0]
        print('  counter: ' + full_line(m, n))
        if 't' in m['records'][n]:
            print('  made at ' + clock_line(m['records'][n]['t']))
        ways(m, n)
    node_ways(m, v)
    want_check(m, ('path', v[0], v[1]), bool(NODE_INDEX.get(v)))
    if v[0] == 0 or v[1] == 0:
        q = abs(v[0]) + abs(v[1])
        facing = 0 if v[0] >= 0 and v[1] == 0 else 1 if v[1] > 0 else 2 if v[0] < 0 else 3
        dh = [d for d in m['divisions'] if d['status'] == 'done' and d['q'] == q]
        print('  Found by splitting and regrouping: %d way(s)' % len(dh))
        for d in dh[:5]:
            print('    ' + division_line(m, d, facing))
        if len(dh) > 5:
            print('    ... and %d more' % (len(dh) - 5))
    hits = [p for p in m['products'] if p['status'] == 'done' and tuple(p['v']) == v]
    print('  Found by repeating adds and turns: %d way(s)' % len(hits))
    for p in hits[:6]:
        print('    ' + product_line(m, p))
    if len(hits) > 6:
        print('    ... and %d more' % (len(hits) - 6))
    if True:
        hits = [r for r in m['slot_log'] if r['status'] == 'done' and r['den'] == 1 and r['value'] == v[0] and r['im'] == v[1]]
        print('  Found in 00404 slot fillings: %d way(s)' % len(hits))
        for r in hits[:5]:
            print('    ' + slot_line(m, r))
        if len(hits) > 5:
            print('    ... and %d more' % (len(hits) - 5))
        want_check(m, ('slot', v[0], 1) if v[1] == 0 else ('cslot', v[0], v[1]), bool(hits))
    plane_point_info(m, v)
    want_check(m, ('plane', v[0], v[1]), v in plane_seen(m))
    return True


HELP = '''
Commands:
  7                  -> how that value was made
  show 12            -> show record #12
  recent             -> the newest records
  stats              -> totals
  roles              -> what the engine was given and what it found
  recipes            -> the S steps and i turns that made each role emerge
  who 1234           -> find ANY record by its global id: family, run, time, recipe
  node 40            -> how path node #40 was reached
  times 3 4          -> repeat the add of 3, 4 times (and turn 3, 4 times)
  div 12 5           -> split 12 units into groups of 5 and count them
  1/2  7/2  -3/4     -> look up a fraction: every leftover and slot filling that makes it
  fractions          -> leftover parts: totals and newest
  2+x=5   x-3=1      -> the blank: which x fits (tried, never solved)
  unk 3 7            -> try the blank for the pair 3 and 7 now
  blanks             -> blank searches: totals and newest
  deadlocks          -> ways back that hit a blocked move, kept in their own library
  solve              -> finish the work already in hand first (no new counter records or pairs)
  tangents           -> branches off main paths, kept in their own library
  approaches         -> paths that close in on a value without arriving, kept in their own library
  differences        -> the change between neighbouring products, kept in their own library
  totals             -> parts stacked onto a growing whole, kept in their own library
  corrections        -> every error that was caught, who caught it, how it was fixed
  correction Luke | what was wrong | how fixed   -> add one
  provenance         -> whose is what: Luke's rule, the coded procedure, what the engine earned
  wanted             -> what was asked for and not found yet (wanted found = answered)
  i*x=1  x+2i=3-i    -> the blank on the plane (points with i): which reached points fit
  solve i*x=1        -> try that plane blank now (a new equation: only tried, never forced)
  proofs             -> slot fillings with one number hidden and found again
  prove 42 1         -> hide number 1 of slot filling 42 and find it now
  pblanks            -> plane blank searches: totals and newest
  plane 6            -> the engine LOOKS at its plane, 6 out each way (1 to 15)
  planes             -> plane points: totals and newest
  2+3i  -4i  -2-2i   -> also says where that point sits on the plane
  divisions          -> splits and regroups: totals and newest
  products           -> repeated adds and turns: totals and newest
  slots              -> the 00404 slot machine: state and newest fillings
  slot 12            -> slot filling #12
  -1  i  -i  2+3i    -> every path that reaches that value
  pair 3 4           -> walk S forward 4 times from 3, right now
  zero               -> what has passed through Z0
  clocks             -> the four clocks right now
  replay  (or check) -> the engine re-checks its whole archive from 0 (the full, slow check)
  export             -> write a readable (uncompressed) copy of the archive to look at or share
  run                -> do another batch now
  help               -> this list
  (just press ENTER to quit)
'''


def _main_gated():
    m = load_memory()
    if m is None:
        print('Stopped.')
        return
    print('DRAGON Z %s - built up from the zero gate' % VERSION)
    print('  >>> ' + GATE_NOTE)
    print('Given: 0 (Z0), S (the counter), the i turn and the 00404 slot template. Everything else must emerge.')
    print('Multiplication emerges from repeating addition; division from splitting units with zeros; fractions from the leftovers.')
    print('Memory:', memory_path())
    GATE['m'] = m
    explore(m)
    print(HELP)
    while True:
        try:
            text = input('> ').strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not text:
            break
        words = text.lower().split()
        try:
            if words[0] == 'run':
                explore(m)
            elif words[0] == 'stats':
                print_stats(m)
            elif words[0] == 'show' and len(words) == 2:
                if not negative_selector(m, 'show', int(words[1])):
                    print('  ' + full_line(m, int(words[1])))
                    print('\n'.join(identity_lines('record', m['records'][int(words[1])])))
            elif words[0] == 'recent':
                for r in m['records'][-10:]:
                    print('  ' + full_line(m, r['id']))
            elif words[0] == 'roles':
                for r in m['roles']:
                    if r.get('given'):
                        what = ('the turn +1 -> +i -> -1 -> -i' if r['name'] == 'i'
                                else 'the first slot template, %s' % breakdown(r['name']))
                        print('  %s  GIVEN (%s): %s' % (r['name'], r['rule'], what))
                    elif r.get('kind') == 'node':
                        origin, word = node_word(m, r['evidence'])
                        print('  %s  FOUND at path node #%d (start at %d, then: %s): %s'
                              % (r['name'], r['evidence'], origin, word, r['why']))
                    elif r.get('kind') == 'proof':
                        print('  %s  FOUND in proof %s  (%s)' % (r['name'], proof_line(m, m['proofs'][r['evidence']]).split('   recipe')[0], r['why']))
                    elif r.get('kind') == 'punknown':
                        u = m['punknowns'][r['evidence']]
                        uf = u['forms'][r['form']]
                        print('  %s  FOUND in plane blank #%d: %s  (%s)' % (r['name'], r['evidence'], punknown_line(
                            m, u, (uf['op'], uf['side'])).split('\n')[-1].strip(), r['why']))
                    elif r.get('kind') == 'plane':
                        p = m['planes'][r['evidence']]
                        print('  %s  FOUND at plane point #%d (%s %s): %s'
                              % (r['name'], r['evidence'], value_text(tuple(p['p'])), p['place'], r['why']))
                    elif r.get('kind') == 'unknown':
                        u = m['unknowns'][r['evidence']]
                        print('  %s  FOUND in blank #%d: %s  (%s)' % (r['name'], r['evidence'], unknown_line(
                            m, u, (u['forms'][r['form']]['op'], u['forms'][r['form']]['side'])).split('\n')[-1].strip(), r['why']))
                    elif r.get('kind') == 'fraction':
                        print('  %s  FOUND in fraction #%d: %s  (%s)'
                              % (r['name'], r['evidence'], fraction_line(m, m['fractions'][r['evidence']]).split('   (from')[0], r['why']))
                    elif r.get('kind') == 'division':
                        print('  %s  FOUND in division #%d: %s  (%s)'
                              % (r['name'], r['evidence'], division_line(m, m['divisions'][r['evidence']]).split('   units')[0], r['why']))
                    elif r.get('kind') == 'product':
                        print('  %s  FOUND in product #%d: %s  (%s)'
                              % (r['name'], r['evidence'], product_line(m, m['products'][r['evidence']]).split('   (')[0], r['why']))
                    elif r['name'] == 'add':
                        print('  add  FOUND in walk #%d: %s' % (r['evidence'], expr_text(m['expressions'][r['evidence']])))
                    if 'recipe' in r:
                        print('       recipe: %s' % r['recipe'])
            elif words[0] == 'times' and len(words) == 3:
                a, b = int(words[1]), int(words[2])
                if not (0 <= a < len(m['records']) and 0 <= b < len(m['records'])):
                    print('  Both must already be counted (0 to %d).' % (len(m['records']) - 1))
                else:
                    do_product(m, a, b, manual=True)
                    print('  ' + product_line(m, m['products'][-2]))
                    print('  ' + product_line(m, m['products'][-1]))
            elif words[0] == 'div' and len(words) == 3:
                a, b = int(words[1]), int(words[2])
                if not (0 <= a < len(m['records']) and 0 <= b < len(m['records'])):
                    print('  Both must already be counted (0 to %d).' % (len(m['records']) - 1))
                else:
                    print('  ' + division_line(m, do_division(m, a, b, manual=True)))
            elif words[0] == 'solve' and len(words) > 1:
                eqt = text[len(text.split()[0]):].strip()
                if parse_equation(eqt) is None:
                    print('  Try something like: solve i*x=1   or   solve x+2i=3-i')
                else:
                    op_, side_, A_, C_ = parse_equation(eqt)
                    if A_ in plane_seen(m) and C_ in plane_seen(m):
                        u_ = do_punknown(m, plane_seen(m)[A_], plane_seen(m)[C_], manual=True)
                        print('  ' + punknown_line(m, u_, (op_, side_)).replace('\n', '\n  '))
                    else:
                        lookup_punknown(m, eqt, force=True)
            elif words[0] == 'proofs':
                print(proof_status(m))
                for p in m['proofs'][-6:]:
                    print('  ' + proof_line(m, p))
            elif words[0] == 'prove' and len(words) == 3:
                sid_, g_ = int(words[1]), int(words[2])
                if not 0 <= sid_ < len(m['slot_log']) or m['slot_log'][sid_]['status'] != 'done':
                    print('  Pick a slot filling that is done (see slots).')
                elif not 0 <= g_ < len(proof_parts(m, m['slot_log'][sid_])[1]) + 1:
                    print('  That filling has %d numbers (0 to %d).' % (len(proof_parts(m, m['slot_log'][sid_])[1]) + 1, len(proof_parts(m, m['slot_log'][sid_])[1])))
                else:
                    print('  ' + proof_line(m, do_proof(m, sid_, g_, manual=True)))
            elif words[0] == 'pblanks':
                print(punknown_status(m))
                for u in m['punknowns'][-3:]:
                    print('  ' + punknown_line(m, u).replace('\n', '\n  '))
            elif words[0] == 'totals':
                print(total_status(m))
                for r in m['totals'][-5:]:
                    print('  ' + total_line(m, r))
            elif words[0] == 'differences':
                print(difference_status(m))
                for r in m['differences'][-5:]:
                    print('  ' + difference_line(m, r))
            elif words[0] == 'approaches':
                print(approach_status(m))
                for r in m['approaches'][-5:]:
                    print('  ' + approach_line(m, r))
            elif words[0] == 'tangents':
                print(tangent_status(m))
                for t in m['tangents'][-5:]:
                    print('  ' + tangent_line(m, t))
            elif words[0] == 'solve':
                solve_tasks(m)
            elif words[0] == 'deadlocks':
                print(deadlock_status(m))
                for r in m['deadlocks'][-5:]:
                    print('  ' + deadlock_line(r))
            elif words[0] == 'corrections':
                print(correction_status(m))
                for c in m['corrections']:
                    print('  ' + correction_line(c).replace('\n', '\n  '))
            elif words[0] == 'correction':
                parts = [p.strip() for p in text[len('correction'):].split('|')]
                if len(parts) != 3 or parts[0] not in CORRECTION_WHO or not parts[1] or not parts[2]:
                    print('  Use: correction WHO | WHAT WAS WRONG | HOW IT WAS FIXED   (WHO is Luke, tests or a Dragon Z version such as Dragon Z v23.1)')
                else:
                    c = add_correction(m, parts[0], 'claim' if parts[1].lower().startswith('claim') else 'code', parts[1], parts[2])
                    print('  Kept: ' + correction_line(c).replace('\n', '\n  '))
            elif words[0] == 'provenance':
                show_provenance(m)
            elif words[0] == 'wanted':
                ws = m['wanted']
                print(wanted_status(m))
                show = [w for w in ws if w['status'] == ('found' if 'found' in words[1:] else 'open')]
                for w in show[-10:]:
                    ans = '' if w['status'] == 'open' else '  -> found in run %d by %s #%d' % (w['found_run'], w['by'][0], w['by'][1])
                    print('  #%d  %s   asked %d time(s)%s' % (w['id'], w['text'], w['asks'], ans))
                if not show:
                    print('  Nothing here yet.')
            elif words[0] in ('plane', 'look'):
                r = int(words[1]) if len(words) > 1 else 5
                if not 1 <= r <= 15:
                    print('  Pick a size from 1 to 15.')
                else:
                    v = do_look(m, r)
                    print('  Look #%d at the plane, %d points reached so far (O = Z0, # = reached, . = not yet):' % (v['id'], v['n']))
                    for row in v['rows']:
                        print('  ' + row)
                    print(plane_status(m))
            elif words[0] == 'planes':
                print(plane_status(m))
                for p in m['planes'][-8:]:
                    print('  point #%d  %s  (%s)  first path node #%d   recipe: %s' % (
                        p['id'], value_text(tuple(p['p'])), p['place'], p['node'], p['recipe']))
            elif words[0] == 'unk' and len(words) == 3:
                a, b = int(words[1]), int(words[2])
                if not (0 <= a < len(m['records']) and 0 <= b < len(m['records'])):
                    print('  Both must already be counted (0 to %d).' % (len(m['records']) - 1))
                elif slots_waiting(m):
                    print('  Waiting for these to be found first:', ' '.join(slots_waiting(m)))
                else:
                    print('  ' + unknown_line(m, do_unknown(m, a, b, manual=True)).replace('\n', '\n  '))
            elif words[0] == 'blanks':
                us = m['unknowns']
                print(unknown_status(m))
                for u in us[-3:]:
                    print('  ' + unknown_line(m, u).replace('\n', '\n  '))
            elif words[0] == 'fractions':
                fr = m['fractions']
                print('  %d leftover parts | %d distinct values | %d written in fewer parts'
                      % (len(fr), len(set(tuple(f['key']) for f in fr)), sum(1 for f in fr if f['g'] >= 2)))
                for f in fr[-8:]:
                    print('  ' + fraction_line(m, f))
            elif words[0] == 'divisions':
                ds = m['divisions']
                print('  %d records | done %d, blocked %d | with a remainder: %d'
                      % (len(ds), sum(1 for d in ds if d['status'] == 'done'),
                         sum(1 for d in ds if d['status'] == 'blocked'), sum(1 for d in ds if d['rem'])))
                for d in ds[-8:]:
                    print('  ' + division_line(m, d))
            elif words[0] == 'products':
                prods = m['products']
                print('  %d records | multiply done: %d, parked: %d | rotate: %d'
                      % (len(prods), sum(1 for p in prods if p['kind'] == 'multiply' and p['status'] == 'done'),
                         len(m['mul_parked']), sum(1 for p in prods if p['kind'] == 'rotate')))
                for p in prods[-8:]:
                    print('  ' + product_line(m, p))
            elif words[0] == 'slots':
                show_slots(m)
            elif words[0] == 'slot' and len(words) == 2:
                if not negative_selector(m, 'slot', int(words[1])):
                    print('  ' + slot_line(m, m['slot_log'][int(words[1])]))
            elif words[0] == 'who' and len(words) == 2:
                fam, r = find_gid(m, int(words[1]))
                if r is None:
                    print('  No record has global id %s.' % words[1])
                else:
                    print('  %s %s' % (fam, {k: v for k, v in r.items() if k not in ('t', 'z0u', 'recipe')}))
                    print('\n'.join(identity_lines(fam, r)))
            elif words[0] == 'recipes':
                recipes_report(m)
            elif words[0] == 'node' and len(words) == 2:
                nid = int(words[1])
                if not negative_selector(m, 'node', nid):
                    origin, word = node_word(m, nid)
                    n = m['nodes'][nid]
                    print('  node #%d  start at %d, then: %s  =  %s  (facing %s)%s'
                          % (nid, origin, word, value_text(node_value(n['c'])), ('+1', '+i', '-1', '-i')[n['d']],
                             '  [a unit cancelled to Z0 here]' if n['cx'] else ''))
            elif words[0] == 'pair' and len(words) == 3:
                a, b = int(words[1]), int(words[2])
                if not (0 <= a < len(m['records']) and 0 <= b < len(m['records'])):
                    print('  Both must already be counted (0 to %d).' % (len(m['records']) - 1))
                else:
                    e = walk_pair(m, a, b)
                    e['manual'] = True        # asked for by hand, so it sits outside the pair order
                    print('  #%d  %s' % (e['id'], expr_text(e)))
            elif words[0] in ('clock', 'time'):
                print('  ' + clock_line(read_clocks(m)))
            elif words[0] == 'zero':
                z = zero_state(m)
                print('  Rule:', z['rule'])
                print_stats(m)
            elif words[0] == 'clocks':
                print('  ' + clock_line(read_clocks(m)))
            elif words[0] in ('replay', 'check'):
                replay_report(m)
            elif words[0] == 'export':
                p_, n_ = export_plain(m)
                print('  Wrote a readable copy: %s (%.1f MB). The engine never reads it back.' % (p_, n_ / 1e6))
            elif words[0] == 'help':
                print(HELP)
            elif not lookup(m, text):
                print('Not understood. Type help for commands.')
        except Exception as exc:                 # a bad command is reported, never the end of the run
            print('Could not do that (%s): %s' % (exc.__class__.__name__, exc))
    resolve_wanted(m)
    if save_memory(m):
        print('Bye. Everything is saved.')
    else:
        print('Bye. Nothing new was saved (see above). The last good files are untouched.')


def main():
    try:
        return _main_gated()
    finally:
        flush_inner()
        GATE['m'] = None


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nStopped. Nothing half-done was saved; the files on disk are as the last good save left them.')
