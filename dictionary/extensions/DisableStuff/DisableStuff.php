<?php

function fnDisableImages( &$skin, &$title, &$file, &$frameParams, &$handlerParams, &$time, &$res ) {
$res="&nbsp;";
return false;
}

// And the function
function efRemoveRedlinks( $skin, $target, &$text, &$customAttribs, &$query, &$options, &$ret ) {
	global $wgUser; # always show for logged in users
	if ( $wgUser->isLoggedIn()) {
		return true; 
	}

	// return immediately if we know it's real
	if ( in_array( 'known', $options ) ) {
		return true; 
	}
	// or if we know it's broken
	if ( in_array( 'broken', $options ) ) {
		$ret = $text;
		return false;
	}
	// hopefully we don't have to do this, but here we'll check for existence.
	// dupes a bit of the logic in Linker::link(), but we have to know here
	if( $target->isKnown() ) {
		return true;
	} else {
		$ret = $text;
		return false;
	}
}

$wgHooks['ImageBeforeProduceHTML'][] = 'fnDisableImages';
$wgHooks['LinkBegin'][] = 'efRemoveRedlinks';


?>
