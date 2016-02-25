#undef TRACEPOINT_PROVIDER
#define TRACEPOINT_PROVIDER cyclictest

#if !defined(_TRACEPOINT_CYCLICTEST_H) || defined(TRACEPOINT_HEADER_MULTI_READ)
#define _TRACEPOINT_CYCLICTEST_H

#include <lttng/tracepoint.h>

TRACEPOINT_EVENT(cyclictest, wait,
	TP_ARGS(int, id),
	TP_FIELDS(
		ctf_integer(int, id, id)
	)
)

TRACEPOINT_EVENT(cyclictest, run,
	TP_ARGS(int, id),
	TP_FIELDS(
		ctf_integer(int, id, id)
	)
)

TRACEPOINT_EVENT(cyclictest, outlier,
	TP_ARGS(int, id),
	TP_FIELDS(
		ctf_integer(int, id, id)
	)
)

TRACEPOINT_EVENT(cyclictest, snapshot_begin,
	TP_ARGS(),
	TP_FIELDS()
)

TRACEPOINT_EVENT(cyclictest, snapshot_end,
	TP_ARGS(),
	TP_FIELDS()
)

#endif /* _TRACEPOINT_CYCLICTEST_H */

#undef TRACEPOINT_INCLUDE
#define TRACEPOINT_INCLUDE "./src/cyclictest/tp.h"
#include <lttng/tracepoint-event.h>
