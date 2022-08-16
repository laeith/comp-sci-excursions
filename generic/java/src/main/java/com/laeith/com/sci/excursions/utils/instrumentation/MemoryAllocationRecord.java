package com.laeith.com.sci.excursions.utils.instrumentation;

import com.laeith.com.sci.excursions.utils.StackTrace;

public record MemoryAllocationRecord(String type, int count, Object object, long size, StackTrace stackTrace) {
}
