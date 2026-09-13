from mni.core import UserState,Intervention,estimate_struggle,recovery_probability,choose_minimum_intervention,intervention_debt

def test_struggle_increases_with_errors():
    assert estimate_struggle(UserState(errors=4,progress_ratio=.5))>estimate_struggle(UserState(errors=0,progress_ratio=.5))

def test_recovery_monotone_in_intervention():
    vals=[recovery_probability(.7,a,.5) for a in Intervention]
    assert vals==sorted(vals)

def test_minimum_intervention_meets_threshold():
    a,p=choose_minimum_intervention(.6,threshold=.70,skill=.55)
    assert p>=.70 or a==Intervention.AUTOMATE

def test_selector_is_minimal():
    a,p=choose_minimum_intervention(.4,threshold=.65,skill=.6)
    if int(a)>0:
        prev=Intervention(int(a)-1)
        assert recovery_probability(.4,prev,.6)<.65

def test_intervention_debt_nonnegative():
    assert intervention_debt([Intervention.HINT,Intervention.GUIDE],[.5,1.0])>=0
