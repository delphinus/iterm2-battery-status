#import <Foundation/Foundation.h>
#import <IOKit/ps/IOPowerSources.h>
#import <IOKit/ps/IOPSKeys.h>

void setStrValue(char **dest, const char *src) {
	int len = strlen(src) + 1;
	*dest = (char*)calloc(len, sizeof(char));
	strncpy(*dest, src, len);
}

void battery(int *percentage, int *elapsed, char **status, char **error) {

	CFTypeRef powerInfo = IOPSCopyPowerSourcesInfo();
	CFArrayRef powerSrcList = IOPSCopyPowerSourcesList(powerInfo);
	CFDictionaryRef powerSrcInfo = NULL;

	if (!powerSrcList) {
		if (powerInfo) CFRelease(powerInfo);
		setStrValue(error, "Failed to get value from IOPSCopyPowerSourcesList()");
		return;
	}

	const void *powerSrcVal = NULL;
	const char *powerStatus = NULL;
	if (CFArrayGetCount(powerSrcList)) {
		powerSrcInfo = IOPSGetPowerSourceDescription(powerInfo, CFArrayGetValueAtIndex(powerSrcList, 0));
		powerSrcVal = CFDictionaryGetValue(powerSrcInfo, CFSTR(kIOPSCurrentCapacityKey));
		CFNumberGetValue((CFNumberRef)powerSrcVal, kCFNumberIntType, percentage);

		powerSrcVal = CFDictionaryGetValue(powerSrcInfo, CFSTR(kIOPSTimeToEmptyKey));
		CFNumberGetValue((CFNumberRef)powerSrcVal, kCFNumberIntType, elapsed);

		powerSrcVal = CFDictionaryGetValue(powerSrcInfo, CFSTR(kIOPSPowerSourceStateKey));
		powerStatus = CFStringGetCStringPtr((CFStringRef)powerSrcVal, kCFStringEncodingUTF8);
		setStrValue(status, powerStatus);
	} else {
		setStrValue(error, "Could not get power resource infomation");
		return;
	}

    if (powerInfo) CFRelease(powerInfo);
    if (powerSrcList) CFRelease(powerSrcList);
}

// vim:se ts=4 sts=4 sw=4 noet:
