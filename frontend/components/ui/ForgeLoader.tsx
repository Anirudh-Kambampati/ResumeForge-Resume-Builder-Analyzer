const SHEET = "M18 14h20l12 12v32a4 4 0 0 1-4 4H18a4 4 0 0 1-4-4V18a4 4 0 0 1 4-4z";

/**
 * Themed loading indicator: a little resume sheet with a face that hops, blinks and
 * throws off a spark at the top of each hop (see .rf-loader in globals.css).
 * Sticker colours are fixed in both themes, like LogoMark. Pass a className such as
 * "h-4 w-4" for inline use in buttons; pass a label for block/page loading states.
 */
export default function ForgeLoader({
  label,
  srLabel = "Loading",
  className = "h-16 w-16",
}: {
  label?: string;
  srLabel?: string;
  className?: string;
}) {
  return (
    <span
      role="status"
      aria-label={label ? undefined : srLabel}
      className="rf-loader inline-flex shrink-0 flex-col items-center justify-center gap-3"
    >
      <svg viewBox="0 0 64 72" className={`overflow-visible ${className}`} aria-hidden="true" focusable="false">
        <ellipse className="rf-loader-ground" cx="32" cy="67" rx="15" ry="3" />
        <g className="rf-loader-body">
          <path transform="translate(3 3)" d={SHEET} fill="#1f1b16" />
          <path d={SHEET} fill="#fffdf8" stroke="#1f1b16" strokeWidth="3.5" strokeLinejoin="round" />
          <path d="M38 14v8a4 4 0 0 0 4 4h8" fill="none" stroke="#1f1b16" strokeWidth="3.5" strokeLinejoin="round" />
          <g className="rf-loader-eyes" fill="#1f1b16">
            <circle cx="25" cy="37" r="2.8" />
            <circle cx="39" cy="37" r="2.8" />
          </g>
          <ellipse cx="20.5" cy="43" rx="3" ry="1.9" fill="#ff9b8a" />
          <ellipse cx="43.5" cy="43" rx="3" ry="1.9" fill="#ff9b8a" />
          <path d="M29 42.5q3 3.4 6 0" fill="none" stroke="#1f1b16" strokeWidth="2.4" strokeLinecap="round" />
          <path className="rf-loader-hl" d="M21 53h22" stroke="#ffd84d" strokeWidth="5" strokeLinecap="round" />
          <path d="M22 53h12" stroke="#1f1b16" strokeWidth="2.6" strokeLinecap="round" />
        </g>
        <path
          className="rf-loader-spark"
          d="M54 -3l2.4 6 5.6 2.4-5.6 2.4-2.4 6-2.4-6-5.6-2.4 5.6-2.4z"
          fill="#bf3119"
          stroke="#1f1b16"
          strokeWidth="1.6"
          strokeLinejoin="round"
        />
      </svg>
      {label && <span className="font-hand text-xl text-zinc-400">{label}</span>}
    </span>
  );
}
