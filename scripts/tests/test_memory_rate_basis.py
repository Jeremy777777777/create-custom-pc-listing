import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))
from memory_rate_basis import validate


def ledger(rate=5600, clock=2.8):
    entries = [('Memory Speed', rate, 'Source design transfer rate'),
               ('Memory Speed Unit', 'MT/s', ''),
               ('Memory Clock Speed', clock, 'Conditional runtime clock'),
               ('Memory Clock Speed Unit', 'GHz', '')]
    facts = [dict(id=str(i), sheet='Product Details', attribute=a,
                  final_value=None, value_candidate=v, source='https://example.test/memory',
                  value_candidate_source='https://example.test/memory',
                  evidence={'candidate_rationale': reason})
             for i, (a, v, reason) in enumerate(entries)]
    return {'amazon_selection': {}, 'facts': facts,
            'fields': [dict(sheet=f['sheet'], attribute=f['attribute'], selected_fact=f['id'])
                       for f in facts]}


class MemoryRateBasisTests(unittest.TestCase):
    def test_half_rate_without_inference_words_is_rejected(self):
        for rate, clock in ((5600, 2.8), (8533, 4.2665), (8400, 4.2), (8448, 4.224)):
            with self.subTest(rate=rate), self.assertRaisesRegex(ValueError, 'transfer-to-clock'):
                validate(ledger(rate, clock))

    def test_both_clock_candidates_from_transfer_source_rejected(self):
        d = ledger(); d['facts'][0]['value_candidate'] = 2800
        d['facts'][1]['value_candidate'] = 'MHz'
        d['facts'][0]['evidence']['candidate_rationale'] = 'DDR 5600 MT/s corresponds to2600MHz; inference'
        with self.assertRaisesRegex(ValueError, 'transfer-to-clock'): validate(d)

    def test_compact_units_and_conditional_ddr_conversion_are_rejected(self):
        for text in ('5600MT/s; a2800MHz clock follows double-data-rate interpretation',
                     'DDR5-4800 data rate; DDR conversion suggests2400MHz'):
            d = ledger(); d['facts'][0]['value_candidate'] = 2800; d['facts'][1]['value_candidate'] = 'MHz'
            d['facts'][0]['evidence']['candidate_rationale'] = text
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, 'transfer-to-clock'): validate(d)

    def test_explicit_unranked_transfer_variants_remain_research_references(self):
        d = ledger(); d['facts'][0]['value_candidate'] = '4400 or 5200'
        d['facts'][0]['evidence']['candidate_rationale'] = 'TIED_VARIANT_DEPENDENT: two official variants, current unit unresolved'
        d['facts'][2].pop('value_candidate'); validate(d)
        d['facts'][0]['evidence']['candidate_rationale'] = 'Unexplained guess'
        with self.assertRaises(ValueError): validate(d)

    def test_qualified_transfer_reference_preserves_history_without_mutation(self):
        d = ledger(); d['facts'][2]['value_candidate'] = 5600; d['facts'][3]['value_candidate'] = 'MT/s'
        d['facts'][2]['evidence']['prior_rate_interpretation'] = ledger()['facts'][2]
        old = copy.deepcopy(d); validate(d); self.assertEqual(d, old)

    def test_actual_clock_requires_bound_independent_basis_when_transfer_is_mentioned(self):
        d = ledger(); f = d['facts'][2]
        f['evidence']['memory_clock_basis'] = dict(kind='MEASURED_CURRENT_CLOCK', value=2.8,
            unit='GHz', source='https://example.test/memory', excerpt='Synthetic measurement: clock2.8GHz')
        validate(d)
        for change in ({'kind': 'CALCULATED'}, {'value': 5600}, {'unit': 'MT/s'},
                       {'source': 'https://different.test'}, {'excerpt': ''}):
            bad = copy.deepcopy(d); bad['facts'][2]['evidence']['memory_clock_basis'].update(change)
            with self.subTest(change=change), self.assertRaises(ValueError): validate(bad)

    def test_oem_quoted_mhz_is_not_blanket_converted(self):
        d = ledger(); d['facts'][0]['value_candidate'] = 3200; d['facts'][1]['value_candidate'] = 'MHz'
        d['facts'][0]['evidence']['candidate_rationale'] = 'Manufacturer lists3200MHz'
        d['facts'][2].pop('value_candidate'); validate(d)

    def test_invalid_rate_unit_and_numbers_fail_without_touching_legacy(self):
        for value, unit in ((-1, 'MT/s'), (float('inf'), 'MT/s'), (True, 'MHz'), (5600, None)):
            d = ledger(); d['facts'][0]['value_candidate'] = value; d['facts'][1]['value_candidate'] = unit
            with self.subTest(value=value), self.assertRaises(ValueError): validate(d)
        d = ledger(); d.pop('amazon_selection'); validate(d)


if __name__ == '__main__': unittest.main()
