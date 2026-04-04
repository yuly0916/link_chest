/**
 * 문자열을 특정 길이만큼 자르고 줄임표(...)를 붙여주는 함수
 * @param {string} str - 원본 문자열
 * @param {number} n - 자를 기준 숫자 (글자 수)
 * @returns {string} - 변환된 문자열
 */
export function truncate(str, n=10) {
  // 1. 예외 처리: 문자열이 없거나 기준 숫자보다 짧으면 그대로 반환
  if (!str || str.length <= n) {
    return str;
  }
  
  // 2. n번째 글자까지 자르고 뒤에 '...'을 붙여서 반환
  return str.slice(0, n) + '...';
}