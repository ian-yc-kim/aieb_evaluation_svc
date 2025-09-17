import uuid
from src.aieb_evaluation_svc.models import Agent, EvaluationCriteria, Evaluation

def test_create_and_read_models(db_session):
    # Create an Agent
    agent_name = f"test-agent-{uuid.uuid4()}"
    new_agent = Agent(name=agent_name)
    db_session.add(new_agent)
    db_session.commit()
    db_session.refresh(new_agent)

    assert new_agent.id is not None
    assert new_agent.name == agent_name

    # Create EvaluationCriteria linked to the Agent
    new_criteria = EvaluationCriteria(
        agent_id=new_agent.id,
        version=1,
        criteria_content="Test criteria content."
    )
    db_session.add(new_criteria)
    db_session.commit()
    db_session.refresh(new_criteria)

    assert new_criteria.id is not None
    assert new_criteria.agent_id == new_agent.id
    assert new_criteria.version == 1

    # Create an Evaluation linked to the EvaluationCriteria
    new_evaluation = Evaluation(
        criteria_id=new_criteria.id,
        agent_prompt="What is the capital of France?",
        agent_output="Paris.",
        results={'accuracy': 1.0}
    )
    db_session.add(new_evaluation)
    db_session.commit()
    db_session.refresh(new_evaluation)

    assert new_evaluation.id is not None
    assert new_evaluation.criteria_id == new_criteria.id
    assert new_evaluation.status == 'pending'
    assert new_evaluation.results['accuracy'] == 1.0

    # Verify objects can be queried
    retrieved_agent = db_session.query(Agent).filter_by(id=new_agent.id).one()
    assert retrieved_agent.name == agent_name

    retrieved_criteria = db_session.query(EvaluationCriteria).filter_by(id=new_criteria.id).one()
    assert retrieved_criteria.criteria_content == "Test criteria content."

    retrieved_evaluation = db_session.query(Evaluation).filter_by(id=new_evaluation.id).one()
    assert retrieved_evaluation.agent_prompt == "What is the capital of France?"
