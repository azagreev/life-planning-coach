/**
 * LPC Wiki Cleanup — Google Apps Script
 *
 * Purpose:
 *   life-planning-coach skill uses append-only file pattern in Google Drive Wiki
 *   (Hot_Cache_{TS}.md, Goals_{TS}.md, etc.) because MCP Drive connector has no
 *   update_file / delete_file tools (verified PoC 2026-05-26 on Claude Max plan,
 *   see docs/research/mcp_poc_log.md §Drive PoC).
 *
 *   This script trashes old timestamped snapshots, keeping last N versions
 *   per prefix and any snapshot newer than RETENTION_DAYS — so Drive Wiki
 *   doesn't accumulate indefinitely.
 *
 * Setup (one-time, ~3 min):
 *   1. Open https://script.google.com → New project
 *   2. Paste entire contents of this file into Code.gs
 *   3. Edit WIKI_FOLDER_NAME below if your wiki folder is named differently
 *   4. Run installTrigger() once (you'll be asked to authorize Drive access)
 *   5. Verify: View → Executions → see cleanupLpcWiki ran without errors
 *   6. Forget about it — daily trigger handles cleanup automatically
 *
 * Customization:
 *   - RETENTION_DAYS: snapshots newer than this many days are always kept
 *   - MIN_RETAIN_PER_PREFIX: minimum number of recent snapshots to keep per category
 *   - PREFIXES: file name prefixes that count as snapshots (extend if you add categories)
 *
 * Safety:
 *   - Only operates inside WIKI_FOLDER_NAME folder (and its subfolders)
 *   - Only touches files starting with one of PREFIXES
 *   - Uses setTrashed(true) — files go to Drive trash (recoverable for 30 days
 *     in Drive UI), never permanently deleted
 *   - Daily Raw_Session_* files NOT touched (they're per-session journal, not snapshots)
 */

const WIKI_FOLDER_NAME = 'Life Planning Coach Wiki';
const RETENTION_DAYS = 30;
const MIN_RETAIN_PER_PREFIX = 5;

// File name prefixes that LPC skill uses for append-only snapshots.
// If skill adds new categories, extend this list.
const PREFIXES = [
  'Hot_Cache_',
  'Goals_',
  'Dashboard_',
  'Progress_Dashboard_',
  'Wheel_of_Life_History_',
  'Core_Values_Compass_',
  'USER_PROGRESS_JOURNAL_',
  'dashboard_data_',
];

/**
 * Main cleanup function. Runs daily via installed trigger.
 */
function cleanupLpcWiki() {
  const folders = DriveApp.getFoldersByName(WIKI_FOLDER_NAME);
  if (!folders.hasNext()) {
    Logger.log('No "%s" folder found. Skipping cleanup.', WIKI_FOLDER_NAME);
    return;
  }
  const wikiFolder = folders.next();
  const cutoff = new Date(Date.now() - RETENTION_DAYS * 86400000);
  let totalTrashed = 0;
  let totalKept = 0;

  PREFIXES.forEach(prefix => {
    const matchingFiles = collectFilesByPrefix(wikiFolder, prefix);
    if (matchingFiles.length === 0) return;

    // Newest first
    matchingFiles.sort((a, b) => b.getLastUpdated() - a.getLastUpdated());

    // Always keep MIN_RETAIN_PER_PREFIX most recent regardless of age
    const candidates = matchingFiles.slice(MIN_RETAIN_PER_PREFIX);
    const toTrash = candidates.filter(f => f.getLastUpdated() < cutoff);

    toTrash.forEach(f => f.setTrashed(true));
    totalTrashed += toTrash.length;
    totalKept += matchingFiles.length - toTrash.length;

    Logger.log('%s: trashed %s, kept %s', prefix, toTrash.length, matchingFiles.length - toTrash.length);
  });

  Logger.log('LPC Wiki cleanup complete. Trashed %s files, kept %s.', totalTrashed, totalKept);
}

/**
 * Recursively collect files matching prefix from folder and subfolders.
 */
function collectFilesByPrefix(folder, prefix) {
  const collected = [];
  const fileIter = folder.searchFiles("title contains '" + prefix + "' and trashed = false");
  while (fileIter.hasNext()) collected.push(fileIter.next());

  const subIter = folder.getFolders();
  while (subIter.hasNext()) {
    const sub = subIter.next();
    collected.push.apply(collected, collectFilesByPrefix(sub, prefix));
  }
  return collected;
}

/**
 * One-time installer. Run this once after pasting the script.
 * Creates a daily trigger that fires cleanupLpcWiki at ~03:00 local time.
 */
function installTrigger() {
  // Remove any existing trigger for this function to avoid duplicates
  ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === 'cleanupLpcWiki')
    .forEach(t => ScriptApp.deleteTrigger(t));

  ScriptApp.newTrigger('cleanupLpcWiki')
    .timeBased()
    .everyDays(1)
    .atHour(3)
    .create();

  Logger.log('Trigger installed. cleanupLpcWiki will run daily at ~03:00.');
}

/**
 * Manual dry-run — logs what WOULD be trashed without actually trashing.
 * Run this first to verify behavior before installing the trigger.
 */
function dryRun() {
  const folders = DriveApp.getFoldersByName(WIKI_FOLDER_NAME);
  if (!folders.hasNext()) {
    Logger.log('No "%s" folder found.', WIKI_FOLDER_NAME);
    return;
  }
  const wikiFolder = folders.next();
  const cutoff = new Date(Date.now() - RETENTION_DAYS * 86400000);

  PREFIXES.forEach(prefix => {
    const matchingFiles = collectFilesByPrefix(wikiFolder, prefix);
    if (matchingFiles.length === 0) return;
    matchingFiles.sort((a, b) => b.getLastUpdated() - a.getLastUpdated());
    const wouldTrash = matchingFiles.slice(MIN_RETAIN_PER_PREFIX)
                                    .filter(f => f.getLastUpdated() < cutoff);
    Logger.log('DRY-RUN %s: would trash %s of %s files',
               prefix, wouldTrash.length, matchingFiles.length);
    wouldTrash.forEach(f => Logger.log('  - %s (modified %s)',
                                       f.getName(), f.getLastUpdated()));
  });
}
