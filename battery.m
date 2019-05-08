#import <Foundation/Foundation.h>
#import <IOKit/ps/IOPowerSources.h>
#import <IOKit/ps/IOPSKeys.h>

struct batteryInfo {
	int percent;
	int elapsed;
	int charging;
	char* status;
	char* error;
};

void setStrValue(char **dest, const char *src) {
	int len = strlen(src) + 1;
	*dest = (char*)calloc(len, sizeof(char));
	strncpy(*dest, src, len);
}

struct batteryInfo battery(void) {
	struct batteryInfo result = {};

	CFTypeRef powerInfo = IOPSCopyPowerSourcesInfo();
	CFArrayRef powerSrcList = IOPSCopyPowerSourcesList(powerInfo);
	CFDictionaryRef powerSrcInfo = NULL;

	if (!powerSrcList) {
		if (powerInfo) CFRelease(powerInfo);
		setStrValue(&result.error, "Failed to get value from IOPSCopyPowerSourcesList()");
		return result;
	}

	const void *powerSrcVal = NULL;
	const char *powerStatus = NULL;
	if (CFArrayGetCount(powerSrcList)) {
		powerSrcInfo = IOPSGetPowerSourceDescription(powerInfo, CFArrayGetValueAtIndex(powerSrcList, 0));
		powerSrcVal = CFDictionaryGetValue(powerSrcInfo, CFSTR(kIOPSCurrentCapacityKey));
		CFNumberGetValue((CFNumberRef)powerSrcVal, kCFNumberIntType, &result.percent);

		powerSrcVal = CFDictionaryGetValue(powerSrcInfo, CFSTR(kIOPSTimeToEmptyKey));
		CFNumberGetValue((CFNumberRef)powerSrcVal, kCFNumberIntType, &result.elapsed);

		powerSrcVal = CFDictionaryGetValue(powerSrcInfo, CFSTR(kIOPSTimeToFullChargeKey));
		CFNumberGetValue((CFNumberRef)powerSrcVal, kCFNumberIntType, &result.charging);

		powerSrcVal = CFDictionaryGetValue(powerSrcInfo, CFSTR(kIOPSPowerSourceStateKey));
		powerStatus = CFStringGetCStringPtr((CFStringRef)powerSrcVal, kCFStringEncodingUTF8);
		setStrValue(&result.status, powerStatus);
	} else {
		setStrValue(&result.error, "Could not get power resource infomation");
		return result;
	}

    if (powerInfo) CFRelease(powerInfo);
    if (powerSrcList) CFRelease(powerSrcList);
	return result;
}

// vim:se ts=4 sts=4 sw=4 noet:
